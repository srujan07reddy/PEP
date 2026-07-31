import yaml
from pathlib import Path
from typing import Dict, Any, List

class DomainValidator:
    """
    Validates a domain package to ensure it complies with the platform's structural and schema requirements.
    """
    def __init__(self):
        pass

    def validate_package(self, package_path: Path) -> Dict[str, Any]:
        """
        Validates the domain package at the given path.
        Returns a dictionary with 'valid' (bool) and 'errors' (list).
        """
        errors = []

        if not package_path.exists() or not package_path.is_dir():
            return {"valid": False, "errors": [f"Package path does not exist or is not a directory: {package_path}"]}

        # 1. Check Manifest
        manifest_path = package_path / "domain_manifest.yaml"
        if not manifest_path.exists():
            errors.append("Missing domain_manifest.yaml")
        else:
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if not data or "domain" not in data:
                        errors.append("Invalid domain_manifest.yaml: Missing root 'domain' key.")
                    else:
                        domain_cfg = data["domain"]
                        if "name" not in domain_cfg:
                            errors.append("Invalid domain_manifest.yaml: Missing 'name' field.")
                        if "version" not in domain_cfg:
                            errors.append("Invalid domain_manifest.yaml: Missing 'version' field.")
                        if "services" not in domain_cfg or not isinstance(domain_cfg["services"], list):
                            errors.append("Invalid domain_manifest.yaml: 'services' must be a list.")
            except Exception as e:
                errors.append(f"Failed to parse domain_manifest.yaml: {e}")

        # 2. Check Requirements
        req_path = package_path / "requirements.yaml"
        if not req_path.exists():
            errors.append("Missing requirements.yaml")

        # 3. Check RBAC
        rbac_path = package_path / "rbac.yaml"
        roles_path = package_path / "roles.yaml"
        if not (rbac_path.exists() or roles_path.exists()):
            errors.append("Missing rbac.yaml or roles.yaml")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
