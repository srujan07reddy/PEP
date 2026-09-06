from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ParserInterface(ABC):
    """
    Abstract base class for all source code syntax parsers (e.g., Tree-sitter).
    Ensures PEP does not depend directly on concrete parser implementations.
    """
    
    @abstractmethod
    def parse(self, source_code: str, language: str) -> Any:
        """Parse source code into an AST."""
        pass
        
    @abstractmethod
    def extract_functions(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract functions from the AST."""
        pass
        
    @abstractmethod
    def extract_classes(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract classes from the AST."""
        pass

    @abstractmethod
    def extract_imports(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract import statements from the AST."""
        pass

    @abstractmethod
    def extract_inheritance(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract class inheritance relationships from the AST."""
        pass

    @abstractmethod
    def extract_call_graph(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract function/method call graphs from the AST."""
        pass

class LSPInterface(ABC):
    """
    Abstract base class for Language Server Protocol (LSP) semantic tools.
    """

    @abstractmethod
    def get_semantic_symbols(self, file_path: str) -> List[Dict[str, Any]]:
        """Retrieve semantic symbols from a file."""
        pass

    @abstractmethod
    def get_references(self, symbol_id: str) -> List[Dict[str, Any]]:
        """Retrieve references to a symbol."""
        pass

    @abstractmethod
    def get_definitions(self, symbol_id: str) -> List[Dict[str, Any]]:
        """Retrieve definitions for a symbol."""
        pass
