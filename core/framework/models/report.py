from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
from .finding import EngineeringRecommendation, Finding
from .maturity import EngineeringMaturityAssessment

class ReportStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"

class AgentReport(BaseModel):
    report_id: str
    agent_name: str
    status: ReportStatus
    findings: List[Finding] = []
    recommendations: List[EngineeringRecommendation] = []
    execution_time_ms: int
    timestamp: str

class Phase(BaseModel):
    name: str
    description: str
    recommendation_ids: List[str]

class TradeOffMatrixEntry(BaseModel):
    recommendation_id: str
    dimension_impacted_positively: List[str]
    dimension_impacted_negatively: List[str]
    trade_off_summary: str

class ERPEvolutionBlueprint(BaseModel):
    # Core Summary
    executive_summary: str
    current_engineering_state: str
    organization_alignment_summary: str
    business_alignment_summary: str
    
    # EMA Component
    maturity_assessment: EngineeringMaturityAssessment
    
    # Matrices
    engineering_dimension_matrix: Dict[str, Dict[str, int]]  # Recommendation ID -> Dimension Scores
    recommendation_matrix: List[EngineeringRecommendation]
    trade_off_matrix: List[TradeOffMatrixEntry]
    engineering_risk_matrix: Dict[str, str]  # Recommendation ID -> Risk Level/Summary
    business_impact_analysis: Dict[str, str]  # Recommendation ID -> Business ROI Summary
    
    # Forward Looking
    implementation_roadmap: List[Phase]
    dependency_graph: Dict[str, List[str]]  # Recommendation ID -> List of Dependent Recommendation IDs
    future_readiness_assessment: str
    continuous_evolution_strategy: str

class MasterReport(BaseModel):
    pipeline_id: str
    target_ref: str
    execution_time_ms: float
    overall_status: ReportStatus
    blueprint: Optional[ERPEvolutionBlueprint] = None
    agent_reports: List[AgentReport]
    timestamp: str
