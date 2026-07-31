class ModelRegistry:
    """
    Maintains a list of allowed models for the platform.
    """
    def __init__(self):
        self.models = {
            "ollama": ["llama3", "mistral", "phi3"],
            "gemini": ["gemini-1.5-pro", "gemini-1.5-flash"],
            "vllm": ["mixtral-8x7b"],
            "openai": ["gpt-4o", "gpt-3.5-turbo"]
        }

    def get_models_for_provider(self, provider: str) -> list:
        return self.models.get(provider, [])
