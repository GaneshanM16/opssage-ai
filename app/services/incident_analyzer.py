from app.config import INCIDENT_DIR, RUNBOOK_DIR, TOP_K_DOCUMENTS
from app.schemas import IncidentAnalysis, RetrievedDocument
from app.services.document_loader import load_markdown_documents
from app.services.embedding import EmbeddingModel
from app.services.llm import generate_analysis
from app.services.vector_store import VectorStore


class IncidentAnalyzer:
    def __init__(self) -> None:
        self.embedding_model = EmbeddingModel()
        self.documents = load_markdown_documents([RUNBOOK_DIR, INCIDENT_DIR])
        document_vectors = self.embedding_model.encode(
            document.text for document in self.documents
        )
        self.vector_store = VectorStore(self.documents, document_vectors)

    def analyze(self, incident: str) -> IncidentAnalysis:
        query_vector = self.embedding_model.encode([incident])[0]
        results = self.vector_store.search(query_vector, TOP_K_DOCUMENTS)
        analysis = generate_analysis(incident, results)

        return IncidentAnalysis(
            summary=_as_text(analysis.get("summary", "")),
            severity=_as_text(analysis.get("severity", "Unknown")),
            probable_causes=_as_list(analysis.get("probable_causes", [])),
            checks=_as_list(analysis.get("checks", [])),
            fix_steps=_as_list(analysis.get("fix_steps", [])),
            incident_report=_as_text(analysis.get("incident_report", "")),
            retrieved_documents=[
                RetrievedDocument(
                    title=result.document.title,
                    source=result.document.source,
                    score=result.score,
                    preview=result.document.text[:300],
                )
                for result in results
            ],
        )


def _as_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "; ".join(f"{key}: {item}" for key, item in value.items())
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [_as_text(item) for item in value]
    if isinstance(value, str):
        return [value]
    return [_as_text(value)]
