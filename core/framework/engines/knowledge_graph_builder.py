import sys
import os
from typing import Any, Dict

# Add the project root to the path so we can import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from registry.adapters.tree_sitter_adapter import TreeSitterAdapter
from registry.adapters.lsp_adapter import LSPAdapter
from core.framework.models.pep_graph import PEPGraph, Node, Edge
from core.framework.models.knowledge_graph import KnowledgeGraph, SemanticSymbol

class KnowledgeGraphBuilder:
    """
    Engine that constructs the Knowledge Graph by orchestrating Tree-sitter and LSP.
    """
    
    def __init__(self):
        self.parser = TreeSitterAdapter()
        self.lsp = LSPAdapter()

    def build(self, repository_path: str, language: str = "python") -> KnowledgeGraph:
        """
        Builds the unified Knowledge Graph for a given repository.
        """
        kg = KnowledgeGraph()
        
        # 1. Syntax Parsing (Tree-sitter) -> PEP Graph
        pep_graph = PEPGraph()
        
        # In a real scenario, we'd walk the repository files
        dummy_file = os.path.join(repository_path, "main.py")
        dummy_source = "def hello(): pass"
        
        ast = self.parser.parse(dummy_source, language)
        
        # Extract features and populate PEP Graph nodes/edges
        functions = self.parser.extract_functions(ast)
        for f in functions:
            node = Node(id=f["name"], type="function", properties=f)
            pep_graph.add_node(node)
            
        classes = self.parser.extract_classes(ast)
        for c in classes:
            node = Node(id=c["name"], type="class", properties=c)
            pep_graph.add_node(node)
            
        calls = self.parser.extract_call_graph(ast)
        for call in calls:
            edge = Edge(source=call["caller"], target=call["callee"], relation="calls")
            pep_graph.add_edge(edge)
            
        kg.merge_pep_graph(pep_graph)

        # 2. Semantic Understanding (LSP) -> Semantic Symbols
        symbols = self.lsp.get_semantic_symbols(dummy_file)
        for sym in symbols:
            s = SemanticSymbol(id=sym["name"], symbol_type=sym["type"], metadata={"location": sym["location"]})
            kg.add_semantic_symbol(s)
            # Link semantic symbol to AST node if they match
            if sym["name"] in pep_graph.nodes:
                kg.link_node_to_symbol(node_id=sym["name"], symbol_id=s.id)
                
        return kg

if __name__ == "__main__":
    builder = KnowledgeGraphBuilder()
    kg = builder.build("d:/product-engineering-platform")
    print("Knowledge Graph built successfully!")
    print(kg.to_dict())
