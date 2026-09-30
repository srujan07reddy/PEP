import tree_sitter
import tree_sitter_python
from typing import Dict, Any, List, Optional
from core.interfaces.code_engine import CodeEngine, CodeGenerationRequest
from core.interfaces.engine import HealthStatus, EngineStatus, BaseEngine
from core.models.code import (
    File, Class, Function, Variable, Import, 
    SourceLocation, Relationship, RelationshipType
)
import uuid

class TreeSitterAdapter(BaseEngine):
    """
    TreeSitter adapter that parses source code and returns the PEP Code Model.
    Currently supports Python extraction and normalization.
    """
    
    def __init__(self):
        self.parser = tree_sitter.Parser()
        self.language = None
        self._is_ready = False
        
    async def initialize(self) -> None:
        """Initialize the Tree-sitter runtime and load the Python grammar."""
        try:
            # Compatible with tree-sitter >= 0.22.0 bindings
            self.language = tree_sitter.Language(tree_sitter_python.language())
            self.parser = tree_sitter.Parser(self.language)
            self._is_ready = True
        except Exception as e:
            self._is_ready = False
            raise RuntimeError(f"Failed to initialize Tree-sitter: {e}")

    async def shutdown(self) -> None:
        """Shutdown parser lifecycle."""
        self.parser = None
        self.language = None
        self._is_ready = False

    def get_health(self) -> HealthStatus:
        if self._is_ready:
            return HealthStatus(status=EngineStatus.READY)
        return HealthStatus(status=EngineStatus.FAILED, message="Parser not initialized")
        
    def get_version(self) -> str:
        return "1.0.0"

    def parse_file(self, source_code: bytes, file_path: str) -> File:
        """
        Parses Python source code and extracts it into the PEP Code Model.
        Handles CST traversal, source locations, extraction, and normalization.
        """
        if not self._is_ready:
            raise RuntimeError("TreeSitterAdapter is not initialized.")
            
        tree = self.parser.parse(source_code)
        
        # Check for parsing errors
        has_errors = tree.root_node.has_error
        
        pep_file = File(
            path=file_path, 
            language="python", 
            name=file_path.split("/")[-1],
            metadata={"has_syntax_errors": has_errors}
        )
        
        # Basic Queries for Python extraction
        class_query = self.language.query("(class_definition name: (identifier) @name) @class")
        func_query = self.language.query("(function_definition name: (identifier) @name) @func")
        import_query = self.language.query("(import_statement name: (dotted_name) @name) @import")
        import_from_query = self.language.query("(import_from_statement module_name: (dotted_name) @module) @import_from")

        # 1. Extract Imports
        for capture, _ in import_query.captures(tree.root_node).items() if hasattr(import_query.captures(tree.root_node), "items") else [((c[0], c[1]), None) for c in import_query.captures(tree.root_node)]:
            # Compatibility wrapper for different tree-sitter bindings
            node, tag = capture[0], capture[1] if isinstance(capture, tuple) else (capture, None)
            if tag == "name" or getattr(capture, "name", None) == "name" or (isinstance(capture, tuple) and capture[1] == "name"):
                n = capture[0] if isinstance(capture, tuple) else capture
                pep_import = Import(
                    name=n.text.decode("utf8"),
                    module=n.text.decode("utf8"),
                    location=self._get_location(n, file_path)
                )
                pep_file.imports.append(pep_import)
                
        # 2. Extract Classes & Methods
        classes_extracted = {}
        for capture in class_query.captures(tree.root_node):
            if isinstance(capture, tuple) and capture[1] == "name":
                node = capture[0]
                class_node = node.parent
                pep_class = Class(
                    name=node.text.decode("utf8"),
                    location=self._get_location(class_node, file_path)
                )
                
                # Extract methods in class (CST traversal)
                for child in class_node.children:
                    if child.type == "block":
                        for block_child in child.children:
                            if block_child.type == "function_definition":
                                func_name_node = block_child.child_by_field_name("name")
                                if func_name_node:
                                    pep_func = Function(
                                        name=func_name_node.text.decode("utf8"),
                                        is_method=True,
                                        location=self._get_location(block_child, file_path)
                                    )
                                    pep_class.functions.append(pep_func)
                
                pep_file.classes.append(pep_class)
                classes_extracted[class_node.id] = pep_class

        # 3. Extract Top-level Functions
        for capture in func_query.captures(tree.root_node):
            if isinstance(capture, tuple) and capture[1] == "name":
                node = capture[0]
                func_node = node.parent
                # Ensure it's not a method (top-level only based on CST)
                if func_node.parent and func_node.parent.type == "module":
                    pep_func = Function(
                        name=node.text.decode("utf8"),
                        is_method=False,
                        location=self._get_location(func_node, file_path)
                    )
                    pep_file.functions.append(pep_func)

        return pep_file

    def _get_location(self, node, file_path: str) -> SourceLocation:
        return SourceLocation(
            start_line=node.start_point[0] + 1,
            start_column=node.start_point[1],
            end_line=node.end_point[0] + 1,
            end_column=node.end_point[1],
            file_path=file_path
        )
