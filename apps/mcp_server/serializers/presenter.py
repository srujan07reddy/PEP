from typing import Dict, Any, Optional
from apps.mcp_server.models.context import AnalysisContext

class AnalysisContextPresenter:
    """
    Read-only presenter responsible for safely serializing rich internal domain models
    (OrganizationKnowledgeModel, KnowledgeGraph, AnalysisResult, Evidence) 
    into an MCP-safe JSON representation, without mutating the internal context.
    """
    
    @staticmethod
    def to_mcp_response(context: AnalysisContext) -> Dict[str, Any]:
        # Start with a base skeleton using Pydantic's safe serialization for built-in models
        business_dict: Dict[str, Any] = {
            "organization": None,
            "processes": context.business.processes
        }
        result: Dict[str, Any] = {
            "identity": context.identity.model_dump(),
            "business": business_dict,
            "code_summary": None,
            "analyses": context.analyses.model_dump(),
            "evidence": context.evidence.model_dump(),
            "metadata": context.metadata
        }
        
        # Safely serialize the rich OrganizationKnowledgeModel if present
        if context.business.organization is not None:
            org = context.business.organization
            if hasattr(org, "model_dump"):
                result["business"]["organization"] = org.model_dump()
            elif hasattr(org, "dict"):
                result["business"]["organization"] = org.dict()
            else:
                # Fallback for non-pydantic objects, though OKM is expected to be Pydantic
                result["business"]["organization"] = str(org)
                
        # Safely summarize the KnowledgeGraph
        # We do not serialize the entire AST to JSON as it would exceed MCP limits,
        # but we expose its metrics and semantic boundaries.
        if context.code is not None:
            kg = context.code
            nodes_count = len(kg.pep_graph.nodes) if hasattr(kg, "pep_graph") and hasattr(kg.pep_graph, "nodes") else 0
            edges_count = len(kg.pep_graph.edges) if hasattr(kg, "pep_graph") and hasattr(kg.pep_graph, "edges") else 0
            symbols_count = len(getattr(kg, "symbols", []))
            
            result["code_summary"] = {
                "nodes_count": nodes_count,
                "edges_count": edges_count,
                "semantic_symbols_count": symbols_count,
                "is_populated": True
            }
            
        return result
