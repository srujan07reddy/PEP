import tree_sitter
import tree_sitter_python
from typing import List, Tuple
from core.framework.compilers.tree_sitter.model import (
    CodeNode, Relationship, FileNode, ClassNode, FunctionNode, 
    VariableNode, ImportNode, SourceLocation, RelationshipType, Parameter
)

class TreeSitterPythonAdapter:
    def __init__(self):
        self.language = tree_sitter.Language(tree_sitter_python.language())
        self.parser = tree_sitter.Parser(self.language)

    def parse_file(self, repository_id: str, file_path: str, source_code: bytes) -> Tuple[List[CodeNode], List[Relationship]]:
        tree = self.parser.parse(source_code)
        root_node = tree.root_node

        nodes: List[CodeNode] = []
        relationships: List[Relationship] = []

        # 1. Create FileNode
        file_loc = SourceLocation(
            file=file_path,
            start_line=root_node.start_point[0] + 1,
            start_col=root_node.start_point[1],
            end_line=root_node.end_point[0] + 1,
            end_col=root_node.end_point[1]
        )
        
        file_id = CodeNode.generate_id(repository_id, file_path, "FILE", file_path)
        file_node = FileNode(
            id=file_id,
            name=file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1],
            language="python",
            location=file_loc,
            size_bytes=len(source_code)
        )
        nodes.append(file_node)

        # 2. Extract Classes
        class_query = tree_sitter.Query(self.language, """
            (class_definition 
                name: (identifier) @name
                superclasses: (argument_list)? @superclasses
            ) @class
        """)
        
        class_cursor = tree_sitter.QueryCursor(class_query)
        for match in class_cursor.matches(root_node):
            captures = match[1]
            if "class" in captures and "name" in captures:
                class_capture = captures["class"][0]
                name_capture = captures["name"][0]
            
                class_name = source_code[name_capture.start_byte:name_capture.end_byte].decode('utf8')
                class_loc = SourceLocation(
                    file=file_path,
                    start_line=class_capture.start_point[0] + 1,
                    start_col=class_capture.start_point[1],
                    end_line=class_capture.end_point[0] + 1,
                    end_col=class_capture.end_point[1]
                )
                class_id = CodeNode.generate_id(repository_id, file_path, "CLASS", class_name)
                
                class_node = ClassNode(
                    id=class_id,
                    name=class_name,
                    language="python",
                    location=class_loc,
                )
                nodes.append(class_node)
                
                relationships.append(Relationship(
                    source_id=file_id,
                    target_id=class_id,
                    type=RelationshipType.CONTAINS
                ))

        # 3. Extract Functions
        func_query = tree_sitter.Query(self.language, """
            (function_definition 
                name: (identifier) @name
                parameters: (parameters) @params
            ) @func
        """)
        
        func_cursor = tree_sitter.QueryCursor(func_query)
        for match in func_cursor.matches(root_node):
            captures = match[1]
            if "func" in captures and "name" in captures:
                func_capture = captures["func"][0]
                name_capture = captures["name"][0]
                    
                func_name = source_code[name_capture.start_byte:name_capture.end_byte].decode('utf8')
                func_loc = SourceLocation(
                    file=file_path,
                    start_line=func_capture.start_point[0] + 1,
                    start_col=func_capture.start_point[1],
                    end_line=func_capture.end_point[0] + 1,
                    end_col=func_capture.end_point[1]
                )
                
                # Check if it's a method by seeing if parent is a block inside a class
                is_method = False
                parent = func_capture.parent
                while parent:
                    if parent.type == "class_definition":
                        is_method = True
                        break
                    parent = parent.parent
                
                func_id = CodeNode.generate_id(repository_id, file_path, "FUNCTION", func_name)
                
                func_node = FunctionNode(
                    id=func_id,
                    name=func_name,
                    language="python",
                    location=func_loc,
                    is_method=is_method
                )
                nodes.append(func_node)
                
                # Determine CONTAINS relationship
                relationships.append(Relationship(
                    source_id=file_id,
                    target_id=func_id,
                    type=RelationshipType.CONTAINS
                ))
                
                if is_method:
                    parent_class = func_capture.parent
                    while parent_class and parent_class.type != "class_definition":
                        parent_class = parent_class.parent
                    
                    if parent_class:
                        c_name_node = parent_class.child_by_field_name("name")
                        if c_name_node:
                            c_name = source_code[c_name_node.start_byte:c_name_node.end_byte].decode('utf8')
                            c_id = CodeNode.generate_id(repository_id, file_path, "CLASS", c_name)
                            relationships.append(Relationship(
                                source_id=c_id,
                                target_id=func_id,
                                type=RelationshipType.CONTAINS
                            ))

        # 4. Extract Calls (Unresolved)
        call_query = tree_sitter.Query(self.language, """
            (call function: (identifier) @target) @call
        """)
        
        call_cursor = tree_sitter.QueryCursor(call_query)
        for match in call_cursor.matches(root_node):
            captures = match[1]
            if "target" in captures and "call" in captures:
                call_capture = captures["call"][0]
                target_capture = captures["target"][0]
            
                target_name = source_code[target_capture.start_byte:target_capture.end_byte].decode('utf8')
                
                # Find enclosing function to set as source_id
                parent = call_capture.parent
                caller_id = file_id
                while parent:
                    if parent.type == "function_definition":
                        caller_name_node = parent.child_by_field_name("name")
                        if caller_name_node:
                            caller_name = source_code[caller_name_node.start_byte:caller_name_node.end_byte].decode('utf8')
                            caller_id = CodeNode.generate_id(repository_id, file_path, "FUNCTION", caller_name)
                            break
                    parent = parent.parent
                    
                relationships.append(Relationship(
                    source_id=caller_id,
                    target_id=f"UNRESOLVED::{target_name}",
                    type=RelationshipType.CALLS
                ))

        return nodes, relationships
