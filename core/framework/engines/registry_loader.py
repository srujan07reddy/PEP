import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class RegistryLoader:
    """
    Parses and caches registry YAML contracts.
    """
    def __init__(self, registry_root_dir: str):
        self.registry_root = Path(registry_root_dir)
        self._cache: Dict[str, Any] = {}

    def load_registry(self, category: str, registry_file: str) -> Optional[Dict[str, Any]]:
        cache_key = f"{category}/{registry_file}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        target_path = self.registry_root / category / registry_file
        if not target_path.exists():
            return None

        with open(target_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self._cache[cache_key] = data
            return data
            
    def clear_cache(self):
        self._cache.clear()
