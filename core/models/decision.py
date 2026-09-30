from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from core.models.assessment import Recommendation

@dataclass
class Alternative:
    """An alternative approach evaluated during the decision-making process."""
    description: str
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)

@dataclass
class Decision:
    """
    The Decision Board Model.
    
    Acts as PEP's highest-level engineering decision interface. 
    It elevates automated findings into a format analogous to a human 
    Architecture Decision Record (ADR), ready for review or autonomous execution.
    """
    problem: str
    recommendation: Recommendation                                 # The final actionable guidance
    evidence_ids: List[str] = field(default_factory=list)          # Traceable Evidence IDs
    affected_systems: List[str] = field(default_factory=list)      # Subsystems, repos, or components
    applicable_standards: List[str] = field(default_factory=list)  # Guiding policies or requirements
    alternatives: List[Alternative] = field(default_factory=list)  # Other options considered
    consequences: List[str] = field(default_factory=list)          # Expected impact of the decision
    confidence: float = 1.0                                        # Overall decision confidence
    
    status: str = "proposed"                                       # 'proposed', 'accepted', 'rejected', 'superseded'
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
