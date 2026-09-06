from typing import Dict, Any, List
from core.framework.models.knowledge_graph import KnowledgeGraph

class SecurityEngine:
    """
    Identifies security risks and anti-patterns in the Knowledge Graph.
    """
    
    def __init__(self):
        pass
        
    def analyze(self, kg: KnowledgeGraph) -> List[Dict[str, Any]]:
        """
        Executes security checks.
        """
        findings = []
        
        # Look for calls to known dangerous functions like eval or exec
        dangerous_functions = {"eval", "exec", "subprocess.call", "os.system"}
        
        for edge in kg.pep_graph.edges:
            if edge.relation == "calls" and edge.target in dangerous_functions:
                findings.append({
                    "engine": "SecurityEngine",
                    "severity": "critical",
                    "message": f"Security Risk: Dangerous function '{edge.target}' is called by '{edge.source}'.",
                    "edge": f"{edge.source}->{edge.target}"
                })
                
        return findings
