from pathlib import Path
from typing import Dict, Any

class WorkspaceRegistry:
    """
    Manages creating code workspaces and attaching them to registered domain packages.
    """
    def __init__(self, workspaces_dir: str, domains_dir: str):
        self.workspaces_dir = Path(workspaces_dir)
        self.domains_dir = Path(domains_dir)
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)

    def register_workspace(self, domain_id: str, absolute_path: str = None) -> Dict[str, Any]:
        """
        Registers a new workspace for a given domain_id.
        """
        # 1. Verify the domain package actually exists in governance/domains
        domain_path = self.domains_dir / domain_id
        if not domain_path.exists():
            return {
                "status": "error",
                "message": f"Cannot create workspace: Domain package '{domain_id}' is not registered."
            }

        workspace_path = self.workspaces_dir / domain_id
        if workspace_path.exists():
            return {
                "status": "error",
                "message": f"Workspace for '{domain_id}' already exists."
            }

        try:
            # 2. Create the workspace folder
            workspace_path.mkdir(parents=True, exist_ok=True)

            # 3. Handle external path mapping if provided
            if absolute_path:
                (workspace_path / ".external_path").write_text(absolute_path.strip(), encoding="utf-8")

            return {
                "status": "success",
                "message": f"Workspace successfully created and attached to domain '{domain_id}'.",
                "workspace_id": domain_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to register workspace: {str(e)}"
            }
