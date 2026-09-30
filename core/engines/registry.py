from typing import Dict, Optional, Type
from core.interfaces.engine import BaseEngine, EngineProvider

class EngineRegistry:
    """Manages the lifecycle and registration of engines and providers."""
    
    def __init__(self):
        self._providers: Dict[str, EngineProvider] = {}
        self._active_engines: Dict[str, BaseEngine] = {}
        
    def register_provider(self, name: str, provider: EngineProvider) -> None:
        self._providers[name] = provider
        
    def get_provider(self, name: str) -> Optional[EngineProvider]:
        return self._providers.get(name)
        
    def register_engine(self, engine_id: str, engine: BaseEngine) -> None:
        self._active_engines[engine_id] = engine
        
    def get_engine(self, engine_id: str) -> Optional[BaseEngine]:
        return self._active_engines.get(engine_id)
        
    async def shutdown_all(self) -> None:
        """Lifecycle method to shutdown all registered engines."""
        for engine in self._active_engines.values():
            await engine.shutdown()
        self._active_engines.clear()
