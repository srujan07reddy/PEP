from typing import Dict, Any
from .contracts import BaseService

class ArchitectureService(BaseService):
    def analyze_architecture(self, domain_id: str) -> Dict[str, Any]:
        """
        Executes architectural analysis using ArchitectureEngine.
        """
        context = self.app.analysis.get_or_create_context(domain_id)
        
        try:
            from core.framework.engines.architecture_engine import ArchitectureEngine
            
            # The ArchitectureEngine strictly requires a KnowledgeGraph.
            if context.code is None:
                return {
                    "status": "failed",
                    "errors": [{"code": "MISSING_DEPENDENCY", "message": "KnowledgeGraph (context.code) is required but missing. GraphService must be run first."}]
                }
                
            kg = context.code
                
            engine = ArchitectureEngine()
            findings = engine.analyze(kg)
            
            context.analyses.architecture = {
                "findings": findings,
                "metrics": {"total_violations": len(findings)}
            }
            
            return {
                "status": "success",
                "data": {
                    "domain_id": domain_id,
                    "violations": len(findings),
                    "findings": findings
                }
            }
            
        except Exception as e:
            # We preserve upstream discovery data even if this fails
            return {
                "status": "partial_success" if (context.business.organization or context.code) else "failed",
                "errors": [{"code": "ARCHITECTURE_ANALYSIS_FAILED", "message": str(e)}]
            }
