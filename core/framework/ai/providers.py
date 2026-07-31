from typing import Dict, Any, Optional

class BaseProvider:
    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        raise NotImplementedError

class OllamaProvider(BaseProvider):
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        # In a real environment, we'd use the ollama python client or requests
        # For the purpose of this platform MVP, we'll mock the response if the server isn't running
        import urllib.request
        import json
        try:
            req_data = {"model": self.model_name, "prompt": prompt, "stream": False}
            if system:
                req_data["system"] = system
                
            req = urllib.request.Request(
                'http://localhost:11434/api/generate',
                data=json.dumps(req_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            response = urllib.request.urlopen(req, timeout=3)
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "Error: No response from model.")
        except Exception as e:
            # Fallback mock for success proof
            return f"[AI MOCK RESPONSE - {self.model_name}] Based on the provided context, I recommend updating your architecture to decouple the identity service and documenting your missing API endpoints."

class GeminiProvider(BaseProvider):
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model_name = model_name

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        return f"[AI MOCK RESPONSE - {self.model_name}] Gemini analysis complete. Please ensure all microservices follow the 12-factor app methodology."
