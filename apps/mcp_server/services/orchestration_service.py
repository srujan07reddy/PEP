import json
from pathlib import Path
from .contracts import BaseService

class OrchestrationService(BaseService):
    """
    Provides an integration boundary to PEP orchestration engines.
    """
    def run_agent_pipeline(self, domain_id: str) -> str:
        from core.orchestrator.orchestrator import PlatformOrchestrator
        try:
            p = PlatformOrchestrator(Path(self.workspace_root))
            rep = p.execute_pipeline(domain_id)
            return json.dumps({"status": "Pipeline completed", "score": getattr(rep, "overall_status", "UNKNOWN")})
        except Exception as e:
            return f"Pipeline failed: {e}"

    def run_generation_pipeline(self, domain_id: str) -> str:
        from core.orchestrator.generation_orchestrator import GenerationOrchestrator
        try:
            p = GenerationOrchestrator(Path(self.workspace_root))
            rep = p.execute_pipeline(domain_id)
            return json.dumps({"status": "Generation Pipeline completed", "score": getattr(rep, "overall_status", "UNKNOWN")})
        except Exception as e:
            return f"Generation Pipeline failed: {e}"
