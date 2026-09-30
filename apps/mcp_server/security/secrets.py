import os
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

class SecretProvider(ABC):
    @abstractmethod
    def get_secret(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def set_secret(self, key: str, value: str) -> None:
        pass

class EnvironmentSecretProvider(SecretProvider):
    """Retrieves secrets from environment variables."""
    def get_secret(self, key: str) -> Optional[str]:
        return os.getenv(key)
        
    def set_secret(self, key: str, value: str) -> None:
        # Not modifying environment in this provider implementation
        pass

class FileSecretProvider(SecretProvider):
    """Retrieves and stores secrets in a specific file."""
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def get_secret(self, key: str) -> Optional[str]:
        # Simplistic implementation matching the current behavior of .coderabbit_key
        # We ignore the key parameter for now since the file just contains the raw value.
        if self.file_path.exists():
            return self.file_path.read_text(encoding="utf-8").strip()
        return None
        
    def set_secret(self, key: str, value: str) -> None:
        self.file_path.write_text(value.strip(), encoding="utf-8")
