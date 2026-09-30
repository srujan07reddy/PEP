from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class MCPResult(BaseModel):
    """
    Standardized result contract for all MCP tool invocations.
    """
    status: str
    request_id: Optional[str] = None
    workspace_id: Optional[str] = None
    timestamp: Optional[str] = None
    data: Dict[str, Any] = {}
    warnings: List[str] = []
    errors: List[str] = []

class AnalysisResult(MCPResult):
    """
    Extended result contract for analytical capabilities.
    """
    findings: List[Dict[str, Any]] = []
    evidence: List[Dict[str, Any]] = []
    confidence: float = 0.0
