from abc import abstractmethod
from typing import Dict, Any, List, Optional
from core.interfaces.engine import BaseEngine
from dataclasses import dataclass

@dataclass
class CodeGenerationRequest:
    prompt: str
    context_files: List[str]
    language: str

class CodeEngine(BaseEngine):
    """Interface for engines specialized in code generation and manipulation."""
    
    @abstractmethod
    async def generate_code(self, request: CodeGenerationRequest) -> str:
        """Generate code based on prompt and context."""
        pass
        
    @abstractmethod
    async def refactor_code(self, code: str, instructions: str) -> str:
        """Refactor existing code based on instructions."""
        pass
