from pathlib import Path
from typing import Dict, Any
from .contracts import BaseService
from apps.mcp_server.security.path_policy import PathPolicy
import yaml

class WorkspaceService(BaseService):
    """
    Handles discovery and validation of workspaces, domains, and standards.
    This replaces direct filesystem traversal inside server.py.
    """
    
    def __init__(self, settings, app=None):
        super().__init__(settings, app)
        self.path_policy = PathPolicy(self.workspace_root)
        
    def resolve_path(self, relative_path: str) -> Path:
        """Resolves and validates a path against the workspace boundary."""
        return self.path_policy.resolve_path(relative_path)
    
    def list_workspaces(self) -> Dict[str, Any]:
        """List all active workspaces and their mapped domains."""
        workspaces_dir = Path(self.workspace_root) / "workspaces"
        domains_dir = Path(self.workspace_root) / "governance" / "domains"
        
        results = {}
        if workspaces_dir.exists():
            for d in workspaces_dir.iterdir():
                if d.is_dir() and not d.name.startswith('.'):
                    domain_path = domains_dir / d.name
                    results[d.name] = {
                        "mapped": domain_path.exists(),
                        "path": str(d)
                    }
        return results

