import json
import yaml
from pathlib import Path
from typing import Dict, Any
from .contracts import BaseService

class GovernanceService(BaseService):
    """
    Interprets and provides governance data (domains, standards) from the workspace.
    """
    
    def list_domains(self) -> Dict[str, Any]:
        """List all registered Domain Packages and their manifests."""
        domains_dir = Path(self.workspace_root) / "governance" / "domains"
        results = {}
        if domains_dir.exists():
            for d in domains_dir.iterdir():
                if d.is_dir() and not d.name.startswith('.'):
                    manifest_path = d / "domain_manifest.yaml"
                    if manifest_path.exists():
                        try:
                            with open(manifest_path, 'r', encoding='utf-8') as f:
                                results[d.name] = yaml.safe_load(f)
                        except Exception as e:
                            results[d.name] = {"error": str(e)}
        return results

    def list_standards(self) -> Dict[str, Any]:
        """Fetch and parse all platform standards from the PEP governance directory."""
        standards_dir = Path(self.workspace_root) / "governance" / "platform" / "standards"
        results = {}
        if standards_dir.exists():
            for f in standards_dir.glob("*.yaml"):
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        results[f.stem] = yaml.safe_load(file)
                except Exception as e:
                    results[f.stem] = f"Error: {e}"
        return results
