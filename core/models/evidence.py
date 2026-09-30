from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone

@dataclass
class EvidenceLocation:
    """
    Universal locator representing structural bounds.
    Can map to bytes in code ASTs or characters in unstructured text.
    """
    start_index: int
    end_index: int
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    file_path: Optional[str] = None

@dataclass
class Evidence:
    """
    Unified Evidence Model.
    This is the core convergence point of PEP. It normalizes any extraction 
    (from Code Models or Text Models) into a single computable structure, 
    allowing PEP to reason across all forms of organizational knowledge.
    """
    source: str                 # e.g., 'deployment.py', 'database_policy.pdf'
    source_type: str            # e.g., 'code', 'document', 'ticket'
    evidence_type: str          # e.g., 'Function', 'Requirement', 'Rule', 'Class'
    
    extractor: str              # e.g., 'tree_sitter', 'nlp_plus', 'spacy'
    confidence: float           # e.g., 1.0 (deterministic parsing) or 0.85 (statistical)
    
    location: EvidenceLocation  # Precise mapping back to origin
    payload: Any                # Flexible payload containing the knowledge (e.g. "deploy_database" or "DBA approval required")

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
