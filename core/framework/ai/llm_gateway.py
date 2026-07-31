from .providers import BaseProvider, OllamaProvider, GeminiProvider

class LLMGateway:
    """
    Unified entrypoint for AI generation. Routes prompts to the correct provider.
    """
    def __init__(self, default_provider: str = "ollama", default_model: str = "llama3"):
        self.default_provider = default_provider
        self.default_model = default_model

    def _get_provider(self, provider: str, model: str) -> BaseProvider:
        if provider == "ollama":
            return OllamaProvider(model_name=model)
        elif provider == "gemini":
            return GeminiProvider(model_name=model)
        else:
            # Fallback
            return OllamaProvider(model_name=model)

    def generate(self, prompt: str, system: str = None, provider: str = None, model: str = None) -> str:
        p = provider or self.default_provider
        m = model or self.default_model
        
        provider_instance = self._get_provider(p, m)
        return provider_instance.generate(prompt, system=system)
