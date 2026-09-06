from dataclasses import dataclass, field
from typing import Dict, Any, List
from core.framework.models.pep_graph import PEPGraph, Node, Edge

@dataclass
class SemanticSymbol:
    id: str
    symbol_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class KnowledgeGraph:
    """
    The ultimate Knowledge Graph that merges structural syntax (PEPGraph via Tree-sitter)
    with semantic understanding (via LSP).
    """
    def __init__(self):
        self.pep_graph = PEPGraph()
        self.symbols: Dict[str, SemanticSymbol] = {}
        # semantic_links connects graph nodes to their semantic symbols
        self.semantic_links: List[Dict[str, str]] = []

    def merge_pep_graph(self, pep_graph: PEPGraph):
        self.pep_graph = pep_graph

    def add_semantic_symbol(self, symbol: SemanticSymbol):
        self.symbols[symbol.id] = symbol

    def link_node_to_symbol(self, node_id: str, symbol_id: str):
        self.semantic_links.append({"node_id": node_id, "symbol_id": symbol_id})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "syntax_graph": self.pep_graph.to_dict(),
            "semantic_symbols": [s.__dict__ for s in self.symbols.values()],
            "links": self.semantic_links
        }
