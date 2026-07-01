from dataclasses import asdict, dataclass, field
from typing import List

try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:
    BaseModel = None
    Field = None


if BaseModel is not None:
    class IncidentRequest(BaseModel):
        incident: str = Field(..., min_length=5, description="Incident, log, or error text")


    class RetrievedDocument(BaseModel):
        title: str
        source: str
        score: float
        preview: str


    class IncidentAnalysis(BaseModel):
        summary: str
        severity: str
        probable_causes: List[str]
        checks: List[str]
        fix_steps: List[str]
        incident_report: str
        retrieved_documents: List[RetrievedDocument]
else:
    def _field(*args, **kwargs):
        return None


    @dataclass
    class IncidentRequest:
        incident: str


    @dataclass
    class RetrievedDocument:
        title: str
        source: str
        score: float
        preview: str


    @dataclass
    class IncidentAnalysis:
        summary: str
        severity: str
        probable_causes: List[str]
        checks: List[str]
        fix_steps: List[str]
        incident_report: str
        retrieved_documents: List[RetrievedDocument] = field(default_factory=list)

        def model_dump(self) -> dict:
            return asdict(self)
