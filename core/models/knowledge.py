from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import uuid
from core.models.evidence import Evidence

@dataclass
class KnowledgeNode:
    """A node in the Knowledge Graph, wrapping a piece of Evidence."""
    evidence: Evidence
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: str = "generic" # e.g. "Policy", "Implementation", "Role"

@dataclass
class KnowledgeEdge:
    """A semantic relationship between two Knowledge Nodes."""
    source_id: str
    target_id: str
    relation: str # e.g., "implemented_by", "requires", "governs", "violates"
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KnowledgeGraph:
    """
    The PEP Knowledge Model. 
    A unified, queryable graph of interconnected organizational facts.
    """
    nodes: Dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: List[KnowledgeEdge] = field(default_factory=list)

    def add_node(self, node: KnowledgeNode):
        self.nodes[node.id] = node
        
    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float = 1.0, metadata: Optional[Dict] = None):
        self.edges.append(KnowledgeEdge(source_id, target_id, relation, weight, metadata or {}))
        
    def get_edges_for_node(self, node_id: str) -> List[KnowledgeEdge]:
        """Returns all edges connected to a specific node."""
        return [e for e in self.edges if e.source_id == node_id or e.target_id == node_id]
