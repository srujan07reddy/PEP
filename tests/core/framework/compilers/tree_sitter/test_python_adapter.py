import pytest
from core.framework.compilers.tree_sitter.python_adapter import TreeSitterPythonAdapter
from core.framework.compilers.tree_sitter.model import RelationshipType

SAMPLE_CODE = b"""
import os

class AuthManager:
    def authenticate(self, user):
        is_valid = validate_user(user)
        if is_valid:
            log_login(user)
            return True
        return False

def validate_user(user):
    return True
"""

def test_parse_file_extracts_nodes():
    adapter = TreeSitterPythonAdapter()
    nodes, rels = adapter.parse_file("repo_1", "auth.py", SAMPLE_CODE)
    
    # Check for FileNode
    file_nodes = [n for n in nodes if n.node_type == "FILE"]
    assert len(file_nodes) == 1
    assert file_nodes[0].name == "auth.py"
    
    # Check for ClassNode
    class_nodes = [n for n in nodes if n.node_type == "CLASS"]
    assert len(class_nodes) == 1
    assert class_nodes[0].name == "AuthManager"
    
    # Check for FunctionNode
    func_nodes = [n for n in nodes if n.node_type == "FUNCTION"]
    assert len(func_nodes) == 2
    func_names = [n.name for n in func_nodes]
    assert "authenticate" in func_names
    assert "validate_user" in func_names
    
    # Check Relationships
    contains_rels = [r for r in rels if r.type == RelationshipType.CONTAINS]
    # File contains class, File contains function, Class contains function (method)
    assert len(contains_rels) > 0
    
    calls_rels = [r for r in rels if r.type == RelationshipType.CALLS]
    target_ids = [r.target_id for r in calls_rels]
    assert "UNRESOLVED::validate_user" in target_ids
    assert "UNRESOLVED::log_login" in target_ids
