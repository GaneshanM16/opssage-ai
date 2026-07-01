from fastapi import FastAPI

from app.schemas import IncidentAnalysis, IncidentRequest
from app.services.incident_analyzer import IncidentAnalyzer


app = FastAPI(title="OpsSage AI", version="0.1.0")
analyzer = IncidentAnalyzer()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "documents_loaded": len(analyzer.documents),
        "embedding_model": analyzer.embedding_model.name,
    }


@app.post("/analyze-incident", response_model=IncidentAnalysis)
def analyze_incident(request: IncidentRequest) -> IncidentAnalysis:
    return analyzer.analyze(request.incident)

