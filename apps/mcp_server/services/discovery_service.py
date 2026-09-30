from typing import Dict, Any
from .contracts import BaseService
from apps.mcp_server.models.context import AnalysisContext

class DiscoveryService(BaseService):
    def discover_business_system(self, domain_id: str) -> Dict[str, Any]:
        """
        Executes discovery using OrganizationIntelligenceLayer and ProcessIntelligenceEngine.
        """
        context = self.app.analysis.get_or_create_context(domain_id)
        
        try:
            from core.framework.engines.organization_intelligence_layer import OrganizationIntelligenceLayer
            from core.framework.engines.process_intelligence_engine import ProcessIntelligenceEngine
            
            from pathlib import Path
            
            # 1. Organization Knowledge
            org_layer = OrganizationIntelligenceLayer(Path(self.workspace_root))
            okm = org_layer.load_organization_knowledge(domain_id)
            
            # 2. Process Knowledge (using mock/defaults for now)
            proc_engine = ProcessIntelligenceEngine()
            expected_wf = proc_engine.fetch_expected_workflow("http://localhost:8080", domain_id)
            actual_wf = proc_engine.mine_actual_workflow(str(Path(self.workspace_root) / "test_data" / f"{domain_id}_events.csv"))
            
            context.business.organization = okm
            context.business.processes = {
                "expected": expected_wf,
                "actual": actual_wf
            }
            
            return {
                "status": "success",
                "data": {
                    "domain_id": domain_id,
                    "organization_name": okm.name,
                    "processes_expected": len(expected_wf.get("steps", [])),
                    "processes_actual": len(actual_wf.get("steps", []))
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "errors": [{"code": "DISCOVERY_FAILED", "message": str(e)}]
            }
