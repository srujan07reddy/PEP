from typing import Optional
from core.interfaces.text_engine import TextEngine
from core.interfaces.engine import HealthStatus, EngineStatus
from core.models.text import Document, Requirement, TextLocation

class MockTransformerEngine(TextEngine):
    """
    A mock statistical/LLM provider. Proves that the Ensemble engine can 
    consume non-deterministic, probabilistic extraction outputs alongside 
    deterministic (NLP++) rules.
    """
    
    def __init__(self):
        self._is_ready = False

    async def initialize(self) -> None:
        self._is_ready = True

    async def shutdown(self) -> None:
        self._is_ready = False

    def get_health(self) -> HealthStatus:
        return HealthStatus(status=EngineStatus.READY if self._is_ready else EngineStatus.FAILED)

    def get_version(self) -> str:
        return "mock-transformer-1.0.0"
        
    def extract_document(self, text: str, title: str, source_path: str) -> Document:
        if not self._is_ready:
            raise RuntimeError("MockTransformerEngine is not initialized.")
            
        doc = Document(title=title, source_path=source_path)
        
        # Simulating statistical extraction with a lower confidence score
        if "must be deployed" in text.lower():
            req = Requirement(
                text_value="CI/CD Deployment",
                source_document=source_path,
                evidence="Implicit requirement based on semantic similarity",
                confidence=0.75, # Probabilistic score
                location=TextLocation(start_char=0, end_char=30),
                priority="high"
            )
            doc.requirements.append(req)
            
        return doc

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return "Generated mock response"
        
    async def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        return "Summarized mock response"
