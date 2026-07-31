import shutil
from pathlib import Path
from typing import Dict, Any, List

from .domain_validator import DomainValidator

class DomainRegistry:
    """
    Manages the installation and registration of domains into the platform.
    """
    def __init__(self, target_domains_dir: str):
        self.target_domains_dir = Path(target_domains_dir)
        self.validator = DomainValidator()
        self.target_domains_dir.mkdir(parents=True, exist_ok=True)

    def install_domain(self, source_package_path: str) -> Dict[str, Any]:
        """
        Validates and installs an external domain package into the governance/domains directory.
        """
        src_path = Path(source_package_path)
        
        # 1. Validate
        validation_result = self.validator.validate_package(src_path)
        if not validation_result["valid"]:
            return {
                "status": "error",
                "message": "Domain package validation failed.",
                "errors": validation_result["errors"]
            }

        # 2. Extract domain name from manifest to use as folder name
        import yaml
        with open(src_path / "domain_manifest.yaml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            domain_name = data["domain"]["name"]
            
        slug = domain_name.lower().replace(" ", "_").strip()
        dest_path = self.target_domains_dir / slug

        # 3. Register (Copy to domains directory)
        if dest_path.exists():
            return {
                "status": "error",
                "message": f"Domain '{slug}' is already registered."
            }
            
        try:
            shutil.copytree(src_path, dest_path)
            return {
                "status": "success",
                "message": f"Domain '{domain_name}' successfully validated and registered as '{slug}'.",
                "domain_id": slug
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to install domain: {e}"
            }

    def unregister_domain(self, domain_id: str) -> bool:
        """
        Removes a domain from the registry.
        """
        domain_path = self.target_domains_dir / domain_id
        if domain_path.exists():
            shutil.rmtree(domain_path)
            return True
        return False
