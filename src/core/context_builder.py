import os
from typing import List, Dict, Optional


def filter_docs(
    docs: List[Dict],
    folders: Optional[List[str]] = None
) -> List[Dict]:
    """
    Filter documents by folder names.

    Args:
        docs: List of document dictionaries.
        folders: Folder names to keep, e.g. ["architecture", "evaluation"].
                 If None, keep all documents.

    Returns:
        Filtered list of docs.
    """
    if folders is None:
        return docs

    folder_set = set(folders)
    return [doc for doc in docs if doc.get("folder") in folder_set]


def truncate_text(text: str, max_chars: Optional[int] = None) -> str:
    """
    Truncate text if max_chars is provided.
    """
    if max_chars is None:
        return text.strip()

    text = text.strip()
    if len(text) <= max_chars:
        return text

    return text[:max_chars].rstrip() + "\n...[truncated]"


def build_knowledge_context(
    docs: List[Dict],
    folders: Optional[List[str]] = None,
    max_chars_per_doc: Optional[int] = None
) -> str:
    """
    Build a single knowledge context string from loaded docs.

    Args:
        docs: List of document dictionaries. Each doc should contain:
              - filename
              - folder
              - content
        folders: Optional folder filter.
        max_chars_per_doc: Optional max characters to keep per document.

    Returns:
        A formatted context string for prompting or caching.
    """
    selected_docs = filter_docs(docs, folders=folders)

    parts = []

    for doc in selected_docs:
        folder = doc.get("folder", "unknown")
        filename = doc.get("filename", "unknown.md")
        content = doc.get("content", "")

        content = truncate_text(content, max_chars=max_chars_per_doc)

        parts.append(f"[{folder}/{filename}]")
        parts.append(content)
        parts.append("")

    return "\n".join(parts)


def summarize_context_info(context: str) -> Dict[str, int]:
    """
    Return simple statistics for debugging.
    """
    return {
        "chars": len(context),
        "lines": len(context.splitlines()),
    }


def build_context(
    knowledge_dir: str,
    folders: Optional[List[str]] = None,
    max_chars_per_doc: Optional[int] = None
) -> str:
    """
    Load markdown files from knowledge_dir and build a merged context string.
    """
    docs = []

    for root, _, files in os.walk(knowledge_dir):
        for file in files:
            if not file.lower().endswith(".md"):
                continue

            path = os.path.join(root, file)
            rel_folder = os.path.relpath(root, knowledge_dir)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            docs.append({
                "filename": file,
                "folder": rel_folder,
                "content": content,
            })

    return build_knowledge_context(
        docs=docs,
        folders=folders,
        max_chars_per_doc=max_chars_per_doc
    )