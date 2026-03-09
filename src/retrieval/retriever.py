import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer


def load_md_files(knowledge_dir: str):
    files = []
    for root, _, filenames in os.walk(knowledge_dir):
        for fn in filenames:
            if fn.lower().endswith(".md"):
                path = os.path.join(root, fn)
                rel = os.path.relpath(path, knowledge_dir)
                files.append((path, rel))
    return files


def split_md_into_chunks(md_text: str):
    """
    Strategy:
    1) Prefer splitting by '## ' headings
    2) If no '## ' headings exist, use whole body
    Returns list of dict: {title, text}
    """
    text = md_text.replace("\r\n", "\n").replace("\r", "\n").strip()

    if text.startswith("# "):
        text = "\n".join(text.split("\n")[1:])

    parts = re.split(r"\n(?=##\s+)", text)

    chunks = []
    for p in parts:
        p = p.strip()
        if not p:
            continue

        lines = p.split("\n")

        if lines[0].startswith("## "):
            title = lines[0][3:].strip()
            body = "\n".join(lines[1:]).strip()
        else:
            title = ""
            body = p

        if body:
            chunks.append({
                "title": title,
                "text": body
            })

    return chunks


def build_chunk_corpus(knowledge_dir: str):
    """
    Returns:
      chunk_texts: list[str]
      chunk_meta: list[dict] with keys: source, title, idx
    """
    files = load_md_files(knowledge_dir)
    chunk_texts, chunk_meta = [], []

    for abs_path, rel_path in files:
        with open(abs_path, "r", encoding="utf-8") as f:
            md = f.read()

        chunks = split_md_into_chunks(md)

        if not chunks and md.strip():
            chunks = [{"title": "全文", "text": md.strip()}]

        for j, ch in enumerate(chunks, start=1):
            packed = f"[{rel_path}] {ch['title']}\n{ch['text']}".strip()
            chunk_texts.append(packed)
            chunk_meta.append({
                "source": rel_path,
                "title": ch["title"],
                "idx": j
            })

    return chunk_texts, chunk_meta


def load_retriever(knowledge_dir: str, model_name: str = "BAAI/bge-small-zh"):
    """
    Build retriever assets once.
    Returns:
      dict containing model, chunk_texts, chunk_meta, chunk_embs
    """
    chunk_texts, chunk_meta = build_chunk_corpus(knowledge_dir)

    if len(chunk_texts) == 0:
        raise FileNotFoundError(f"No chunks found. Check: {knowledge_dir}")

    model = SentenceTransformer(model_name)
    chunk_embs = model.encode(chunk_texts, normalize_embeddings=True)

    return {
        "model": model,
        "chunk_texts": chunk_texts,
        "chunk_meta": chunk_meta,
        "chunk_embs": chunk_embs,
    }


def search_chunks(query: str, retriever_state: dict, top_k: int = 3):
    """
    Semantic search for top-k relevant chunks.
    Returns list[dict]:
      {
        source,
        title,
        idx,
        score,
        text
      }
    """
    model = retriever_state["model"]
    chunk_texts = retriever_state["chunk_texts"]
    chunk_meta = retriever_state["chunk_meta"]
    chunk_embs = retriever_state["chunk_embs"]

    q = model.encode(query, normalize_embeddings=True)
    scores = chunk_embs @ q

    k = min(top_k, len(scores))
    top_idx = np.argsort(-scores)[:k]

    results = []
    for idx in top_idx:
        meta = chunk_meta[idx]
        results.append({
            "source": meta["source"],
            "title": meta["title"],
            "idx": meta["idx"],
            "score": float(scores[idx]),
            "text": chunk_texts[idx]
        })

    return results


def build_retrieved_context(results: list[str | dict]) -> str:
    """
    Build final prompt context from retrieved results.
    """
    parts = []

    for item in results:
        if isinstance(item, dict):
            text = item["text"]
        else:
            text = item

        parts.append(text.strip())
        parts.append("")

    return "\n".join(parts).strip()


def main():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
    KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "knowledge")

    retriever_state = load_retriever(KNOWLEDGE_DIR)

    print(f"[INFO] Knowledge dir: {KNOWLEDGE_DIR}")
    print(f"[INFO] Chunks: {len(retriever_state['chunk_texts'])}")
    print(f"[INFO] chunk_embs shape: {retriever_state['chunk_embs'].shape}")

    while True:
        query = input("\nQ (type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = search_chunks(query, retriever_state, top_k=3)

        print("\n[RESULT] Top chunks:")
        for rank, item in enumerate(results, start=1):
            body = item["text"].split("\n", 1)
            preview = body[1] if len(body) == 2 else item["text"]
            preview = preview[:360].replace("\n", " ").strip()
            if len(preview) >= 360:
                preview += "..."

            print(f"\n#{rank}  score: {item['score']:.4f}")
            print(
                f"     source: {item['source']}  |  chunk: {item['idx']}  |  title: {item['title']}"
            )
            print(f"     preview: {preview}")


if __name__ == "__main__":
    main()