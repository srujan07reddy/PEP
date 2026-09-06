from typing import Dict, Any, List
from core.framework.models.knowledge_graph import KnowledgeGraph

class ArchitectureEngine:
    """
    Validates system design and dependency rules from the Knowledge Graph.
    """
    
    def __init__(self):
        pass
        
    def analyze(self, kg: KnowledgeGraph) -> List[Dict[str, Any]]:
        """
        Executes architectural checks.
        """
        findings = []
        
        # Detect circular dependencies or unauthorized cross-domain calls
        for edge in kg.pep_graph.edges:
            if edge.relation == "calls":
                # Very simple heuristic: if a controller calls another controller directly, flag it.
                if "controller" in edge.source.lower() and "controller" in edge.target.lower():
                    findings.append({
                        "engine": "ArchitectureEngine",
                        "severity": "high",
                        "message": f"Architectural violation: Controller {edge.source} directly calls Controller {edge.target}.",
                        "edge": f"{edge.source}->{edge.target}"
                    })
                    
        return findings
