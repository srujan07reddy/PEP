import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class StandardsLoader:
    """
    Parses and caches the standard YAML rulebooks.
    """
    def __init__(self, standards_root_dir: str):
        self.standards_root = Path(standards_root_dir)
        self._cache: Dict[str, Any] = {}

    def load_standard(self, domain: str, standard_file: str) -> Optional[Dict[str, Any]]:
        cache_key = f"{domain}/{standard_file}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        target_path = self.standards_root / domain / standard_file
        if not target_path.exists():
            return None

        with open(target_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self._cache[cache_key] = data
            return data
            
    def clear_cache(self):
        self._cache.clear()
