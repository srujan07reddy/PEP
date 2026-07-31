import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class DomainLoader:
    """
    Parses and mounts a domain package manifest into memory.
    """
    def __init__(self, domains_root_dir: str):
        self.domains_root = Path(domains_root_dir)
        self.loaded_domains: Dict[str, Any] = {}

    def load_domain(self, domain_name: str) -> Optional[Dict[str, Any]]:
        if domain_name in self.loaded_domains:
            return self.loaded_domains[domain_name]

        manifest_path = self.domains_root / domain_name / "domain_manifest.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Domain manifest not found for {domain_name} at {manifest_path}")

        domain_package = {}

        # 1. Load Manifest
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            domain_package["manifest"] = data.get("domain", {})
            
        # 2. Load Standards (Requirements)
        req_path = self.domains_root / domain_name / "requirements.yaml"
        if req_path.exists():
            with open(req_path, 'r', encoding='utf-8') as f:
                domain_package["requirements"] = yaml.safe_load(f)

        # 3. Load Permissions (RBAC)
        rbac_path = self.domains_root / domain_name / "rbac.yaml"
        roles_path = self.domains_root / domain_name / "roles.yaml"
        perm_path = rbac_path if rbac_path.exists() else (roles_path if roles_path.exists() else None)
        
        if perm_path:
            with open(perm_path, 'r', encoding='utf-8') as f:
                domain_package["permissions"] = yaml.safe_load(f)
                
        # (Optional) 4. Load Workflows
        workflows_path = self.domains_root / domain_name / "workflows.yaml"
        if workflows_path.exists():
            with open(workflows_path, 'r', encoding='utf-8') as f:
                domain_package["workflows"] = yaml.safe_load(f)

        self.loaded_domains[domain_name] = domain_package
        return domain_package
            
    def get_loaded_domains(self) -> Dict[str, Any]:
        return self.loaded_domains
