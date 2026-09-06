import tree_sitter_python
from tree_sitter import Language, Parser
from typing import Dict, Any, List

class TreeSitterEngine:
    """
    Parses Python source code to extract structured entities (classes, methods, imports, calls)
    for integration into the Knowledge Graph.
    """
    
    def __init__(self):
        self.language = Language(tree_sitter_python.language())
        self.parser = Parser(self.language)

    def _query(self, tree, query_string: str) -> List[Any]:
        query = self.language.query(query_string)
        captures = query.captures(tree.root_node)
        return captures

    def extract_code_entities(self, source_code: bytes, file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parses source code and extracts classes, functions, imports, and calls.
        Returns a dictionary of nodes and edges that can be ingested by the Knowledge Graph.
        """
        tree = self.parser.parse(source_code)
        
        entities = {
            "classes": [],
            "functions": [],
            "imports": [],
            "calls": []
        }

        # 1. Extract Classes
        class_query = "(class_definition name: (identifier) @class_name)"
        for node, tag in self._query(tree, class_query):
            class_name = node.text.decode('utf-8')
            entities["classes"].append({
                "id": f"{file_path}::{class_name}",
                "name": class_name,
                "type": "class",
                "file": file_path
            })

        # 2. Extract Functions/Methods
        func_query = "(function_definition name: (identifier) @func_name)"
        for node, tag in self._query(tree, func_query):
            func_name = node.text.decode('utf-8')
            entities["functions"].append({
                "id": f"{file_path}::{func_name}",
                "name": func_name,
                "type": "function",
                "file": file_path
            })

        # 3. Extract Imports
        import_query = "(import_from_statement module_name: (dotted_name) @module) (import_statement name: (dotted_name) @module)"
        try:
            # Simple fallback since tree-sitter queries can be strict based on syntax
            import_query_obj = self.language.query("(import_from_statement module_name: (dotted_name) @module)")
            for node, tag in import_query_obj.captures(tree.root_node):
                module_name = node.text.decode('utf-8')
                entities["imports"].append({
                    "source": file_path,
                    "target": module_name,
                    "relation": "imports"
                })
        except Exception:
            pass

        # 4. Extract Calls (Function Calls)
        call_query = "(call function: (identifier) @called_func)"
        try:
            for node, tag in self._query(tree, call_query):
                called_func = node.text.decode('utf-8')
                entities["calls"].append({
                    "source": file_path, # In a more complex setup, this would be the enclosing function
                    "target": called_func,
                    "relation": "calls"
                })
        except Exception:
            pass
            
        return entities
