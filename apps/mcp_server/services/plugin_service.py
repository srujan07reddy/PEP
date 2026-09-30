import json
from pathlib import Path
from .contracts import BaseService
from apps.mcp_server.security.secrets import SecretProvider, FileSecretProvider

class PluginService(BaseService):
    """
    Provides an integration boundary for AI providers and external plugins.
    """
    def __init__(self, settings, app=None):
        super().__init__(settings, app)
        # Preserve existing behavior by storing coderabbit key in a dotfile at workspace root.
        # In a real environment this might be injected as a different provider type.
        self.secret_provider: SecretProvider = FileSecretProvider(
            str(Path(self.workspace_root) / ".coderabbit_key")
        )
        
    def set_coderabbit_api_key(self, api_key: str) -> str:
        """Store the CodeRabbit API key."""
        try:
            self.secret_provider.set_secret("coderabbit_api_key", api_key)
            return json.dumps({"status": "API key successfully stored."})
        except Exception as e:
            return f"Error storing API key: {e}"

    def get_code_recommendations(self, filename: str, code_snippet: str) -> str:
        """
        Analyzes a code snippet using all available AI Review Adapters.
        """
        from core.framework.plugins.plugin_manager import PluginManager
        try:
            manager = PluginManager()
            adapters_dir = Path(self.workspace_root) / "registry" / "adapters"
            manager.load_plugins(str(adapters_dir))
            
            reviewers = manager.get_all_adapters("ai_code_review")
            all_findings = []
            
            for reviewer in reviewers:
                try:
                    # In a fully integrated version, we'd pass the secret provider or key to the reviewer
                    findings = reviewer.request_review(code_snippet, filename)
                    all_findings.extend(findings)
                except Exception as e:
                    pass
                    
            return json.dumps({
                "status": "success",
                "findings": all_findings,
                "message": f"Analyzed by {len(reviewers)} AI engines."
            }, indent=2)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
