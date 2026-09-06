from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Node:
    id: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Edge:
    source: str
    target: str
    relation: str
    properties: Dict[str, Any] = field(default_factory=dict)

class PEPGraph:
    """
    Represents the structural graph of the repository based on Syntax (Tree-sitter).
    Nodes can be files, classes, functions, imports.
    Edges represent inheritance, calls, includes.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.__dict__ for n in self.nodes.values()],
            "edges": [e.__dict__ for e in self.edges]
        }
