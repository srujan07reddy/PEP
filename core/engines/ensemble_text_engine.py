from typing import List, Optional
from core.interfaces.text_engine import TextEngine
from core.interfaces.engine import HealthStatus, EngineStatus
from core.models.text import Document, TextElement

class EnsembleTextEngine(TextEngine):
    """
    An orchestrator engine that routes the same text through multiple underlying
    TextEngine providers (e.g., NLP++, spaCy, Transformers) and merges their
    extractions into a single Unified Evidence Model (Document).
    """
    
    def __init__(self, engines: List[TextEngine]):
        self.engines = engines
        self._is_ready = False

    async def initialize(self) -> None:
        """Initialize all underlying engines."""
        for engine in self.engines:
            await engine.initialize()
        self._is_ready = True

    async def shutdown(self) -> None:
        """Shutdown all underlying engines."""
        for engine in self.engines:
            await engine.shutdown()
        self._is_ready = False

    def get_health(self) -> HealthStatus:
        if not self._is_ready:
            return HealthStatus(status=EngineStatus.FAILED, message="Ensemble not initialized.")
            
        for engine in self.engines:
            if engine.get_health().status != EngineStatus.READY:
                return HealthStatus(status=EngineStatus.DEGRADED, message=f"Engine {engine.get_version()} is degraded.")
                
        return HealthStatus(status=EngineStatus.READY)

    def get_version(self) -> str:
        return "ensemble-1.0.0"

    def extract_document(self, text: str, title: str, source_path: str) -> Document:
        """
        Passes the text through all underlying engines and merges the results.
        Combines deterministic (NLP++) and statistical (Transformer) extractions.
        """
        merged_doc = Document(title=title, source_path=source_path)
        
        for engine in self.engines:
            partial_doc = engine.extract_document(text, title, source_path)
            self._merge_documents(merged_doc, partial_doc, engine.get_version())
                
        return merged_doc

    def _merge_documents(self, target: Document, source: Document, engine_id: str):
        """
        Merges elements from the source document into the target document.
        Appends the engine_id to the metadata to track evidence provenance.
        """
        def merge_list(target_list: List[TextElement], source_list: List[TextElement]):
            for item in source_list:
                item.metadata["extracted_by"] = engine_id
                target_list.append(item)

        merge_list(target.entities, source.entities)
        merge_list(target.relations, source.relations)
        merge_list(target.requirements, source.requirements)
        merge_list(target.rules, source.rules)
        merge_list(target.policies, source.policies)
        merge_list(target.constraints, source.constraints)
        merge_list(target.events, source.events)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        raise NotImplementedError("Ensemble is for extraction only.")

    async def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        raise NotImplementedError("Ensemble is for extraction only.")
