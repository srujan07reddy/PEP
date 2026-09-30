from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from core.models.evidence import Evidence
from core.models.knowledge import KnowledgeNode

@dataclass
class Finding:
    """
    A concrete discovery made by an Intelligence Engine based on specific Evidence.
    e.g., "Function deploy_database lacks authorization check."
    """
    description: str
    severity: str # 'low', 'medium', 'high', 'critical'
    evidence_ids: List[str] = field(default_factory=list) # Traceability anchor to Evidence Model
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Recommendation:
    """
    Actionable guidance derived from an Assessment.
    Critically, every recommendation must trace back to the exact evidence and 
    organizational policies that justify it, ensuring 100% explainability.
    """
    action: str
    reasoning: str
    affected_components: List[str] = field(default_factory=list) # Code paths or graph Node IDs
    applicable_policy: Optional[str] = None # The specific Policy node ID or text
    evidence_ids: List[str] = field(default_factory=list) # The raw facts that led here
    confidence: float = 1.0 # E.g., 0.95 confidence in this recommendation
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Assessment:
    """
    A comprehensive evaluation grouping Findings and proposing Recommendations.
    Sits at the top of the traceability hierarchy:
    Evidence -> Finding -> Assessment -> Recommendation
    """
    domain: str # e.g., 'Security', 'Architecture', 'Quality', 'Organization'
    summary: str
    findings: List[Finding] = field(default_factory=list)
    recommendations: List[Recommendation] = field(default_factory=list)
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
