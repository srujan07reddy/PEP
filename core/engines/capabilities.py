from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

class CapabilityType(str, Enum):
    CODE_GENERATION = "code_generation"
    TEXT_GENERATION = "text_generation"
    CODE_ANALYSIS = "code_analysis"
    EMBEDDING = "embedding"

@dataclass
class Capability:
    name: str
    type: CapabilityType
    description: str
    parameters: Dict[str, Any]

@dataclass
class EngineCapabilityModel:
    capabilities: List[Capability]
    max_context_window: int
    supported_languages: List[str]
