import pytest
from pydantic import ValidationError

from core.framework.compilers.tree_sitter.model import (
    SourceLocation,
    CodeNode,
    FileNode,
    ClassNode,
    FunctionNode,
    VariableNode,
    ImportNode,
    Relationship,
    RelationshipType,
    Parameter,
    RepositoryNode,
    ModuleNode
)

def test_source_location_instantiation():
    loc = SourceLocation(file="auth.py", start_line=1, start_col=0, end_line=10, end_col=15)
    assert loc.start_line == 1
    assert loc.end_col == 15
    assert loc.file == "auth.py"

def test_code_node_id_generation():
    node_id = CodeNode.generate_id("repo_1", "/path/to/main.py", "FUNCTION", "login")
    assert isinstance(node_id, str)
    assert len(node_id) > 0

def test_file_node_instantiation():
    loc = SourceLocation(file="/path/to/main.py", start_line=1, start_col=0, end_line=100, end_col=0)
    file_node = FileNode(
        id=CodeNode.generate_id("repo", "/path/to/main.py", "FILE", "main.py"),
        name="main.py",
        language="python",
        location=loc,
        size_bytes=1024
    )
    assert file_node.node_type == "FILE"
    assert file_node.language == "python"

def test_class_node_instantiation():
    loc = SourceLocation(file="main.py", start_line=10, start_col=0, end_line=50, end_col=0)
    class_node = ClassNode(
        id="class_1",
        name="UserManager",
        language="python",
        location=loc,
    )
    assert class_node.node_type == "CLASS"
    assert class_node.name == "UserManager"
    assert class_node.visibility == "public"

def test_function_node_instantiation():
    loc = SourceLocation(file="main.py", start_line=20, start_col=4, end_line=30, end_col=20)
    func_node = FunctionNode(
        id="func_1",
        name="login",
        language="python",
        location=loc,
        parameters=[Parameter(name="username", type_hint="str")],
        return_type_hint="bool",
        is_method=True
    )
    assert func_node.node_type == "FUNCTION"
    assert len(func_node.parameters) == 1
    assert func_node.parameters[0].name == "username"
    assert func_node.is_method is True

def test_relationship_instantiation():
    rel = Relationship(
        source_id="func_1",
        target_id="var_1",
        type=RelationshipType.USES
    )
    assert rel.type == "USES"

def test_invalid_node_type_fails():
    loc = SourceLocation(file="main.py", start_line=1, start_col=0, end_line=10, end_col=15)
    with pytest.raises(ValidationError):
        # Missing required fields like 'size_bytes' should fail
        FileNode(
            id="file_1",
            name="main.py",
            location=loc,
        )
