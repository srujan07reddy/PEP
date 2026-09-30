from abc import abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from core.interfaces.engine import BaseEngine
from core.models.code import CodeEntity, File, Repository, SourceLocation, Relationship

@dataclass
class CallGraph:
    """Represents a graph of function and method calls."""
    edges: List[Relationship] = field(default_factory=list)
    nodes: Dict[str, CodeEntity] = field(default_factory=dict)

    def get_callers(self, target_id: str) -> List[CodeEntity]:
        """Returns all entities that call the given target."""
        caller_ids = [edge.target_id for edge in self.edges if edge.metadata.get("callee") == target_id]
        return [self.nodes[cid] for cid in caller_ids if cid in self.nodes]

    def get_callees(self, source_id: str) -> List[CodeEntity]:
        """Returns all entities called by the given source."""
        callee_ids = [edge.target_id for edge in self.edges if edge.metadata.get("caller") == source_id]
        return [self.nodes[cid] for cid in callee_ids if cid in self.nodes]

@dataclass
class DependencyGraph:
    """Represents a graph of module and file dependencies."""
    edges: List[Relationship] = field(default_factory=list)
    nodes: Dict[str, CodeEntity] = field(default_factory=dict)

    def get_dependencies(self, entity_id: str) -> List[CodeEntity]:
        """Returns all entities the given entity depends on."""
        dep_ids = [edge.target_id for edge in self.edges if edge.metadata.get("source") == entity_id]
        return [self.nodes[did] for did in dep_ids if did in self.nodes]

    def get_dependents(self, entity_id: str) -> List[CodeEntity]:
        """Returns all entities that depend on the given entity."""
        dep_ids = [edge.target_id for edge in self.edges if edge.metadata.get("target") == entity_id]
        return [self.nodes[did] for did in dep_ids if did in self.nodes]

@dataclass
class ModuleRelationship:
    """Represents structural relationships between modules or packages."""
    source_module: str
    target_module: str
    relationship_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class SymbolResolutionInterface:
    """Interface for resolving source locations to semantic symbols."""
    
    @abstractmethod
    async def resolve_symbol(self, file_path: str, line: int, column: int) -> Optional[CodeEntity]:
        """Resolves a specific position in a file to a recognized CodeEntity."""
        pass

class ReferenceTrackingInterface:
    """Interface for tracking usages and references of symbols."""
    
    @abstractmethod
    async def find_references(self, entity_id: str) -> List[SourceLocation]:
        """Finds all usages of a specific code entity across the repository."""
        pass

class SemanticEnrichmentEngine(BaseEngine):
    """
    Engine responsible for taking a base structural Code Model (e.g., from Tree-sitter)
    and enriching it with semantic relationships, reference tracking, and graph construction.
    """
    
    @abstractmethod
    async def enrich_repository(self, repository: Repository) -> Repository:
        """Enriches the entire repository model with semantic data."""
        pass
        
    @abstractmethod
    async def build_call_graph(self, repository: Repository) -> CallGraph:
        """Extracts and builds the complete call graph for the repository."""
        pass
        
    @abstractmethod
    async def build_dependency_graph(self, repository: Repository) -> DependencyGraph:
        """Extracts and builds the module dependency graph."""
        pass
        
    @abstractmethod
    async def get_symbol_resolver(self) -> SymbolResolutionInterface:
        """Returns a provider capable of symbol resolution."""
        pass
        
    @abstractmethod
    async def get_reference_tracker(self) -> ReferenceTrackingInterface:
        """Returns a provider capable of tracking symbol references."""
        pass
