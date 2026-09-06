from abc import ABC, abstractmethod
from typing import List, Any

class BasePlugin(ABC):
    """
    Base interface for all PEP adapters and plugins.
    Ensures that plugins self-report their identity and capabilities.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Returns the unique name of the plugin."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Returns the version of the plugin."""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Returns a list of capability strings.
        Example: ["ast_parsing", "graph_database", "process_mining"]
        """
        pass

    @abstractmethod
    def initialize(self) -> bool:
        """
        Setup any resources required by the plugin.
        Returns True if successful, False otherwise.
        """
        pass
