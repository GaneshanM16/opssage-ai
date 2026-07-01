from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Document:
    title: str
    source: str
    text: str


def load_markdown_documents(paths: Iterable[Path]) -> List[Document]:
    documents: List[Document] = []

    for folder in paths:
        if not folder.exists():
            continue

        for file_path in sorted(folder.glob("*.md")):
            text = file_path.read_text(encoding="utf-8").strip()
            if not text:
                continue

            title = _extract_title(text, file_path.stem)
            documents.append(
                Document(title=title, source=str(file_path), text=text)
            )

    return documents


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        clean_line = line.strip()
        if clean_line.startswith("# "):
            return clean_line[2:].strip()
    return fallback.replace("_", " ").title()

