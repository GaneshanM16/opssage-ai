import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import INCIDENT_DIR, RUNBOOK_DIR
from app.services.document_loader import load_markdown_documents
from app.services.embedding import EmbeddingModel
from app.services.vector_store import VectorStore


def main() -> None:
    documents = load_markdown_documents([RUNBOOK_DIR, INCIDENT_DIR])
    model = EmbeddingModel()
    vectors = model.encode(document.text for document in documents)
    VectorStore(documents, vectors)

    print(f"Loaded documents: {len(documents)}")
    print(f"Embedding model: {model.name}")
    print("Vector store created successfully.")


if __name__ == "__main__":
    main()
