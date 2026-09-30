from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from core.models.knowledge import KnowledgeGraph, KnowledgeNode, KnowledgeEdge

class KnowledgeStore(ABC):
    """
    The PEP Knowledge Interface.
    Abstracts away the underlying storage infrastructure (Graph, Vector, Search, Relational).
    Ensures that PEP's logic is never coupled to a specific database vendor.
    """
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the storage provider."""
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the storage provider."""
        pass
        
    @abstractmethod
    async def save_graph(self, graph: KnowledgeGraph) -> None:
        """Persist a compiled Knowledge Graph into storage."""
        pass
        
    @abstractmethod
    async def query_nodes(self, query: Dict[str, Any]) -> List[KnowledgeNode]:
        """Query for specific nodes based on metadata, embeddings, or exact match."""
        pass
        
    @abstractmethod
    async def get_subgraph(self, root_node_id: str, depth: int = 1) -> KnowledgeGraph:
        """Retrieve a subgraph originating from a specific node."""
        pass
