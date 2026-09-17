import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class ProviderAdapter(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def validate(self, api_key: str) -> bool:
        """Stage 2: Provider-specific verification via official API."""
        pass

    @abstractmethod
    def get_models(self, api_key: str) -> List[Dict[str, Any]]:
        """Stage 3: Discover accessible models."""
        pass

    @abstractmethod
    def get_model_limits(self, api_key: str, model: str) -> Dict[str, Any]:
        """Get limits for a specific model."""
        pass

    @abstractmethod
    def get_usage(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Stage 4: Fetch usage information if exposed."""
        pass

    @abstractmethod
    def get_quota(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Fetch quota information if exposed."""
        pass

    @abstractmethod
    def get_rate_limits(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Fetch rate limits if exposed."""
        pass

class OpenAIAdapter(ProviderAdapter):
    @property
    def provider_name(self) -> str: return "openai"

    def validate(self, api_key: str) -> bool:
        try:
            resp = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            return resp.status_code == 200
        except Exception:
            return False

    def get_models(self, api_key: str) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                models = []
                for m in data:
                    models.append({
                        "id": m.get("id"),
                        "context_limit": None, # OpenAI API doesn't return context limits in /v1/models directly
                        "max_output_tokens": None
                    })
                return models
        except Exception:
            pass
        return []

    def get_model_limits(self, api_key: str, model: str) -> Dict[str, Any]:
        return {"context_limit": None, "max_output_tokens": None}

    def get_usage(self, api_key: str) -> Optional[Dict[str, Any]]:
        # Requires organization/project endpoint, returning None safely
        return None

    def get_quota(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

    def get_rate_limits(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

class AnthropicAdapter(ProviderAdapter):
    @property
    def provider_name(self) -> str: return "anthropic"

    def validate(self, api_key: str) -> bool:
        try:
            resp = requests.get(
                "https://api.anthropic.com/v1/organizations/me",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                timeout=5
            )
            # 200 is admin, 403 might be valid normal access but lacking org permissions
            # Anthropic returns 401 for invalid keys
            return resp.status_code in (200, 403)
        except Exception:
            return False

    def get_models(self, api_key: str) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(
                "https://api.anthropic.com/v1/models",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                models = []
                for m in data:
                    models.append({
                        "id": m.get("id"),
                        "context_limit": None,
                        "max_output_tokens": None
                    })
                return models
        except Exception:
            pass
        return []

    def get_model_limits(self, api_key: str, model: str) -> Dict[str, Any]:
        return {"context_limit": None, "max_output_tokens": None}

    def get_usage(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

    def get_quota(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

    def get_rate_limits(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

class GeminiAdapter(ProviderAdapter):
    @property
    def provider_name(self) -> str: return "gemini"

    def validate(self, api_key: str) -> bool:
        try:
            resp = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models",
                headers={"x-goog-api-key": api_key},
                timeout=5
            )
            return resp.status_code == 200
        except Exception:
            return False

    def get_models(self, api_key: str) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models",
                headers={"x-goog-api-key": api_key},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json().get("models", [])
                models = []
                for m in data:
                    models.append({
                        "id": m.get("name", "").replace("models/", ""),
                        "context_limit": m.get("inputTokenLimit"),
                        "max_output_tokens": m.get("outputTokenLimit")
                    })
                return models
        except Exception:
            pass
        return []

    def get_model_limits(self, api_key: str, model: str) -> Dict[str, Any]:
        return {"context_limit": None, "max_output_tokens": None}

    def get_usage(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

    def get_quota(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

    def get_rate_limits(self, api_key: str) -> Optional[Dict[str, Any]]:
        return None

def detect_provider(api_key: str) -> Optional[ProviderAdapter]:
    """Stage 1: Offline fingerprinting based on key structure."""
    key = api_key.strip()
    if key.startswith("sk-ant-"):
        return AnthropicAdapter()
    elif key.startswith("sk-") and not key.startswith("sk-ant-"):
        return OpenAIAdapter()
    elif key.startswith("AIza") or key.startswith("AQ"):
        return GeminiAdapter()
    return None
