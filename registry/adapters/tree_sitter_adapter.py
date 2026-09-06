from typing import Any, Dict, List, Optional
import sys
import os
import tree_sitter
import tree_sitter_python

# Add the project root to the path so we can import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.interfaces.parser import ParserInterface
from core.interfaces.plugin import BasePlugin

class TreeSitterAdapter(ParserInterface, BasePlugin):
    """
    Adapter for the tree-sitter library.
    Implements ParserInterface to decouple PEP from tree-sitter specifics.
    """
    
    def get_name(self) -> str:
        return "TreeSitterAdapter"

    def get_version(self) -> str:
        return "1.0.0"

    def get_capabilities(self) -> List[str]:
        return ["ast_parsing"]

    def initialize(self) -> bool:
        # Initialize tree-sitter language bindings
        try:
            self.language_python = tree_sitter.Language(tree_sitter_python.language())
            self.parser = tree_sitter.Parser(self.language_python)
            return True
        except Exception:
            return False

    def __init__(self):
        # Initialize tree-sitter language bindings
        self.language_python = tree_sitter.Language(tree_sitter_python.language())
        self.parser = tree_sitter.Parser(self.language_python)
        
    def parse(self, source_code: str, language: str) -> Any:
        """Parse source code into an AST using tree-sitter."""
        if language.lower() != "python":
            raise ValueError(f"Language {language} is not supported currently.")
        
        # tree-sitter requires bytes
        if isinstance(source_code, str):
            source_bytes = source_code.encode("utf-8")
        else:
            source_bytes = source_code
            
        return self.parser.parse(source_bytes)

    def _traverse_and_collect(self, node, node_type: str, collected: List[Any]):
        """Helper to recursively collect nodes of a specific type."""
        if node.type == node_type:
            collected.append(node)
        for child in node.children:
            self._traverse_and_collect(child, node_type, collected)

    def _get_node_text(self, node, source_bytes: bytes) -> str:
        """Extract text for a node."""
        if not node:
            return ""
        return source_bytes[node.start_byte:node.end_byte].decode("utf-8")

    def extract_functions(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract functions from the AST."""
        functions = []
        function_nodes = []
        self._traverse_and_collect(ast.root_node, "function_definition", function_nodes)
        
        source_bytes = ast.root_node.text if hasattr(ast.root_node, "text") and isinstance(ast.root_node.text, bytes) else b""
        if not source_bytes and hasattr(ast, "_source_bytes"):
            source_bytes = ast._source_bytes
            
        # We need a robust way to get text. Let's just use the root_node.text which in tree_sitter python bindings is sometimes available,
        # but properly we should pass source bytes or extract it.
        # Tree-sitter nodes have a .text attribute in recent versions.
        
        for node in function_nodes:
            name_node = node.child_by_field_name("name")
            name = name_node.text.decode('utf-8') if name_node and hasattr(name_node, 'text') else ""
            functions.append({
                "name": name,
                "type": "function",
                "start_point": node.start_point,
                "end_point": node.end_point
            })
        return functions
        
    def extract_classes(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract classes from the AST."""
        classes = []
        class_nodes = []
        self._traverse_and_collect(ast.root_node, "class_definition", class_nodes)
        
        for node in class_nodes:
            name_node = node.child_by_field_name("name")
            name = name_node.text.decode('utf-8') if name_node and hasattr(name_node, 'text') else ""
            classes.append({
                "name": name,
                "type": "class",
                "start_point": node.start_point,
                "end_point": node.end_point
            })
        return classes

    def extract_imports(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract import statements from the AST."""
        imports = []
        import_nodes = []
        self._traverse_and_collect(ast.root_node, "import_statement", import_nodes)
        self._traverse_and_collect(ast.root_node, "import_from_statement", import_nodes)
        
        for node in import_nodes:
            text = node.text.decode('utf-8') if hasattr(node, 'text') else ""
            imports.append({
                "module": text,
                "type": "import",
                "start_point": node.start_point,
                "end_point": node.end_point
            })
        return imports

    def extract_inheritance(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract class inheritance relationships from the AST."""
        inheritance = []
        class_nodes = []
        self._traverse_and_collect(ast.root_node, "class_definition", class_nodes)
        
        for node in class_nodes:
            name_node = node.child_by_field_name("name")
            name = name_node.text.decode('utf-8') if name_node and hasattr(name_node, 'text') else ""
            
            bases_node = node.child_by_field_name("superclasses")
            inherits_from = []
            if bases_node:
                # Iterate over arguments in the argument list
                for child in bases_node.children:
                    if child.type == "identifier":
                        inherits_from.append(child.text.decode('utf-8') if hasattr(child, 'text') else "")
                        
            if inherits_from:
                inheritance.append({
                    "class": name,
                    "inherits_from": inherits_from
                })
        return inheritance

    def extract_call_graph(self, ast: Any) -> List[Dict[str, Any]]:
        """Extract function/method call graphs from the AST."""
        calls = []
        
        def traverse_calls(node, current_func=""):
            new_func = current_func
            if node.type == "function_definition":
                name_node = node.child_by_field_name("name")
                if name_node and hasattr(name_node, 'text'):
                    new_func = name_node.text.decode('utf-8')
                    
            if node.type == "call":
                func_node = node.child_by_field_name("function")
                callee = ""
                if func_node:
                    if func_node.type == "identifier":
                        callee = func_node.text.decode('utf-8') if hasattr(func_node, 'text') else ""
                    elif func_node.type == "attribute":
                        attr_name = func_node.child_by_field_name("attribute")
                        if attr_name:
                            callee = attr_name.text.decode('utf-8') if hasattr(attr_name, 'text') else ""
                
                if callee:
                    calls.append({
                        "caller": current_func or "<module>",
                        "callee": callee
                    })
                    
            for child in node.children:
                traverse_calls(child, new_func)
                
        traverse_calls(ast.root_node)
        return calls
