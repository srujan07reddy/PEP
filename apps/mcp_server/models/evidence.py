from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

class SourceLocation(BaseModel):
    file: Optional[str] = None
    symbol: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    column: Optional[int] = None

class Provenance(BaseModel):
    engine: str
    extractor: str
    workspace_fingerprint: str
    analysis_timestamp: str

class Evidence(BaseModel):
    id: str
    type: str # e.g., code_symbol, document, interview
    subject: str
    observation: str
    source: SourceLocation
    provenance: Provenance
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Finding(BaseModel):
    id: str
    type: str
    severity: str # high, medium, low
    title: str
    description: str
    evidence_refs: List[str]
    confidence: float # 0.0 to 1.0 representing confidence in the validity of the observation/inference

    @field_validator('confidence')
    @classmethod
    def check_confidence(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v

class EvidenceStore(BaseModel):
    observations: List[Evidence] = Field(default_factory=list)
    findings: List[Finding] = Field(default_factory=list)
