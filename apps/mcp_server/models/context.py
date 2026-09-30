from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from apps.mcp_server.models.evidence import EvidenceStore

class ContextIdentity(BaseModel):
    workspace_id: str
    workspace_root: str
    fingerprint: str

class BusinessContext(BaseModel):
    organization: Optional[Any] = None # OrganizationKnowledgeModel
    processes: Dict[str, Any] = Field(default_factory=dict)

class AnalysisResults(BaseModel):
    architecture: Optional[Any] = None
    workflow: Optional[Any] = None
    governance: Optional[Any] = None
    security: Optional[Any] = None

class AnalysisContext(BaseModel):
    """
    A small, immutable-ish carrier for analysis state.
    Used to prevent redundant workspace scanning by downstream engines.
    """
    identity: ContextIdentity
    
    business: BusinessContext = Field(default_factory=BusinessContext)
    code: Optional[Any] = None              # CodeDependencyGraph / KnowledgeGraph
    
    analyses: AnalysisResults = Field(default_factory=AnalysisResults)
    evidence: EvidenceStore = Field(default_factory=EvidenceStore)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
