from pathlib import Path
from typing import List, Dict


def load_docs(base_dir: str = "knowledge/ml") -> List[Dict]:
    """
    Load all markdown documents under the given knowledge directory.

    Args:
        base_dir: Base directory containing knowledge documents.

    Returns:
        A list of document dictionaries with:
            - filepath
            - filename
            - folder
            - relative_path
            - content
    """
    docs_dir = Path(base_dir)

    if not docs_dir.exists():
        raise FileNotFoundError(f"Directory not found: {docs_dir}")

    docs = []

    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")

        docs.append({
            "filepath": str(path),
            "filename": path.name,
            "folder": path.parent.name,
            "relative_path": str(path.relative_to(docs_dir)),
            "content": text
        })

    return docs


def load_docs_by_extension(
    base_dir: str = "knowledge/ml",
    extension: str = "*.md"
) -> List[Dict]:
    """
    Load documents by a specific file extension pattern.

    Args:
        base_dir: Base directory containing documents.
        extension: File pattern, e.g. "*.md", "*.txt".

    Returns:
        A list of document dictionaries.
    """
    docs_dir = Path(base_dir)

    if not docs_dir.exists():
        raise FileNotFoundError(f"Directory not found: {docs_dir}")

    docs = []

    for path in sorted(docs_dir.rglob(extension)):
        text = path.read_text(encoding="utf-8")

        docs.append({
            "filepath": str(path),
            "filename": path.name,
            "folder": path.parent.name,
            "relative_path": str(path.relative_to(docs_dir)),
            "content": text
        })

    return docs


def summarize_docs(docs: List[Dict]) -> Dict[str, int]:
    """
    Return simple document statistics for debugging.
    """
    return {
        "num_docs": len(docs),
        "total_chars": sum(len(doc.get("content", "")) for doc in docs),
    }