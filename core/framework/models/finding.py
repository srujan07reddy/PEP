from pydantic import BaseModel
from typing import List, Dict, Optional
from .dimensions import EngineeringDimension
from .rule import RuleSeverity

# --- LEGACY MODELS (For backward compatibility with existing agents) ---
class FindingSource(BaseModel):
    agent_name: str
    rule_id: str

class Location(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    context_snippet: Optional[str] = None

class Finding(BaseModel):
    id: str
    severity: RuleSeverity
    title: str
    description: str
    recommendation: str
    source: FindingSource
    location: Location
    timestamp: str
    
# --- NEW EDF MODELS ---

class RecommendationPriority(BaseModel):
    level: str  # Critical, High, Medium, Low
    confidence_score: float

class TradeOff(BaseModel):
    benefit: str
    drawback: str

class BusinessImpact(BaseModel):
    business_value: str
    engineering_value: str
    operational_value: str
    user_value: str
    implementation_cost: str
    engineering_effort: str
    estimated_timeline: str
    expected_roi: str
    expected_risk_reduction: str

class EngineeringDimensionScorecard(BaseModel):
    dimension_scores: Dict[EngineeringDimension, int]
    overall_impact_score: int
    projected_maturity_impact: Dict[str, float]

class EngineeringRecommendation(BaseModel):
    id: str
    title: str
    summary: str
    problem_statement: str
    current_situation: str
    observed_evidence: str
    root_cause: str
    recommended_solution: str
    alternative_solutions: List[str]
    
    # Context Mapping
    applicable_engineering_principles: List[str]
    applicable_organizational_policies: List[str]
    applicable_workflows: List[str]
    applicable_architecture: List[str]
    
    trade_offs: List[TradeOff]
    
    implementation_strategy: str
    dependencies: List[str]
    
    priority: RecommendationPriority
    business_impact: BusinessImpact
    dimension_scorecard: EngineeringDimensionScorecard
    
    future_impact: List[str]
    timestamp: str
