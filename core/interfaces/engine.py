from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

class EngineStatus(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"
    SHUTDOWN = "shutdown"

@dataclass
class HealthStatus:
    status: EngineStatus
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

@dataclass
class VersionCompatibility:
    min_version: str
    max_version: Optional[str] = None
    tested_versions: List[str] = None

class EngineError(Exception):
    """Base error model for all engine operations."""
    def __init__(self, message: str, code: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

class EngineProvider(ABC):
    """Provider interface for creating and managing engines."""
    
    @abstractmethod
    def get_provider_name(self) -> str:
        pass
        
    @abstractmethod
    def create_engine(self, config: Dict[str, Any]) -> 'BaseEngine':
        pass

class BaseEngine(ABC):
    """Base Engine interface that all specific engines must implement."""
    
    @abstractmethod
    async def initialize(self) -> None:
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        pass
        
    @abstractmethod
    def get_health(self) -> HealthStatus:
        pass
        
    @abstractmethod
    def get_version(self) -> str:
        pass
