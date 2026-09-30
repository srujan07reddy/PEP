from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class EngineMetadata:
    name: str
    version: str
    author: str
    description: str
    tags: list[str]

@dataclass
class EngineConfiguration:
    metadata: EngineMetadata
    provider_config: Dict[str, Any]
    capabilities_config: Dict[str, Any]
    timeouts: Dict[str, int]
    retry_policy: Dict[str, Any]
    is_enabled: bool = True
