from typing import Dict, Any, List, Optional
from core.interfaces.engine import HealthStatus, EngineStatus, BaseEngine
from core.models.code import (
    File, Class, Function, Variable, Import, 
    SourceLocation
)

class MockCodeEngine(BaseEngine):
    """
    A lightweight mock provider that returns deterministic PEP Code Models 
    without actually parsing any real code.
    
    Used to prove that PEP is decoupled from Tree-sitter and can support 
    any provider that conforms to the interface.
    """
    
    def __init__(self):
        self._is_ready = False
        
    async def initialize(self) -> None:
        """Initialize the mock engine immediately."""
        self._is_ready = True

    async def shutdown(self) -> None:
        """Shutdown the mock engine."""
        self._is_ready = False

    def get_health(self) -> HealthStatus:
        if self._is_ready:
            return HealthStatus(status=EngineStatus.READY)
        return HealthStatus(status=EngineStatus.SHUTDOWN)
        
    def get_version(self) -> str:
        return "mock-1.0.0"

    def parse_file(self, source_code: bytes, file_path: str) -> File:
        """
        Returns a hardcoded, mocked File entity representing the Code Model,
        regardless of the input source_code. 
        Proves the orchestration layer just cares about the Output Model.
        """
        if not self._is_ready:
            raise RuntimeError("MockCodeEngine is not initialized.")
            
        file_name = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            
        return File(
            path=file_path,
            language="mocklang",
            name=file_name,
            imports=[
                Import(
                    name="sys",
                    module="sys",
                    location=SourceLocation(1, 0, 1, 11, file_path)
                )
            ],
            classes=[
                Class(
                    name="MockedController",
                    location=SourceLocation(3, 0, 10, 0, file_path),
                    functions=[
                        Function(
                            name="handle_request",
                            is_method=True,
                            location=SourceLocation(5, 4, 8, 16, file_path)
                        )
                    ]
                )
            ],
            functions=[
                Function(
                    name="mocked_utility_function",
                    is_method=False,
                    location=SourceLocation(12, 0, 15, 12, file_path)
                )
            ]
        )
