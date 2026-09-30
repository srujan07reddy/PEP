from abc import abstractmethod
from typing import Dict, Any, List, Optional
from core.interfaces.engine import BaseEngine
from core.models.text import Document

class TextEngine(BaseEngine):
    """Interface for engines specialized in natural language processing."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text based on a prompt."""
        pass
        
    @abstractmethod
    async def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """Summarize the provided text."""
        pass
        
    @abstractmethod
    def extract_document(self, text: str, title: str, source_path: str) -> Document:
        """Extract structured organizational knowledge from text into the PEP Text Model."""
        pass
