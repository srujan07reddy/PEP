from pydantic import BaseModel
from typing import Dict, List

class EngineeringQualityMatrix(BaseModel):
    organization_alignment: float = 0.0
    workflow_alignment: float = 0.0
    policy_alignment: float = 0.0
    architecture_quality: float = 0.0
    governance_quality: float = 0.0
    data_quality: float = 0.0
    ai_readiness: float = 0.0
    integration_quality: float = 0.0
    reliability: float = 0.0
    maintainability: float = 0.0
    future_readiness: float = 0.0

class EvidenceMapping(BaseModel):
    dimension: str
    okm_references: List[str]
    explanation: str

class EngineeringMaturityAssessment(BaseModel):
    current_maturity: EngineeringQualityMatrix
    projected_maturity: EngineeringQualityMatrix
    evidence: List[EvidenceMapping]
