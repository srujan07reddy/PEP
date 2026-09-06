import hashlib
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class SourceLocation(BaseModel):
    """Represents a precise location in a source file."""
    file: str
    start_line: int
    start_col: int
    end_line: int
    end_col: int


class CodeNode(BaseModel):
    """Base class for all PEP Code Model nodes."""
    id: str = Field(..., description="Stable unique identifier derived from type, location, and name")
    name: str = Field(..., description="Name of the node entity")
    language: str = Field(default="unknown", description="Programming language of the node")
    location: Optional[SourceLocation] = None
    node_type: str = Field(..., description="The type of the node")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Language-specific metadata")
    
    @classmethod
    def generate_id(cls, repository_id: str, file_path: str, node_type: str, qualified_name: str) -> str:
        """Helper to generate a stable, reproducible ID."""
        hash_input = f"{repository_id}::{file_path}::{node_type}::{qualified_name}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()


class RepositoryNode(CodeNode):
    node_type: Literal['REPOSITORY'] = 'REPOSITORY'
    # Override name to be the repository name
    repository_path: str


class ModuleNode(CodeNode):
    node_type: Literal['MODULE'] = 'MODULE'
    # Represents a logical module (like a python package)


class FileNode(CodeNode):
    node_type: Literal['FILE'] = 'FILE'
    size_bytes: int


class ClassNode(CodeNode):
    node_type: Literal['CLASS'] = 'CLASS'
    visibility: str = "public"
    base_classes: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None


class Parameter(BaseModel):
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None


class FunctionNode(CodeNode):
    node_type: Literal['FUNCTION'] = 'FUNCTION'
    parameters: List[Parameter] = Field(default_factory=list)
    return_type_hint: Optional[str] = None
    is_async: bool = False
    is_method: bool = False
    docstring: Optional[str] = None


class VariableNode(CodeNode):
    node_type: Literal['VARIABLE'] = 'VARIABLE'
    type_hint: Optional[str] = None
    is_constant: bool = False


class ImportNode(CodeNode):
    node_type: Literal['IMPORT'] = 'IMPORT'
    imported_names: List[str] = Field(default_factory=list)
    alias: Optional[str] = None


class RelationshipType:
    CONTAINS = 'CONTAINS'
    CALLS = 'CALLS'
    USES = 'USES'
    IMPORTS = 'IMPORTS'
    INHERITS = 'INHERITS'
    IMPLEMENTS = 'IMPLEMENTS'
    OVERRIDES = 'OVERRIDES'
    REFERENCES = 'REFERENCES'
    DEPENDS_ON = 'DEPENDS_ON'
    DEFINES = 'DEFINES'
    READS = 'READS'
    WRITES = 'WRITES'
    INSTANTIATES = 'INSTANTIATES'
    THROWS = 'THROWS'
    CATCHES = 'CATCHES'


class Relationship(BaseModel):
    """Represents a directional edge between two CodeNodes."""
    source_id: str
    target_id: str
    type: str = Field(..., description="Must be one of RelationshipType constants, or extensible string")
    metadata: Dict[str, Any] = Field(default_factory=dict)
