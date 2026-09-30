from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid

@dataclass
class SourceLocation:
    """Represents a specific location within a source file."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    file_path: str

class RelationshipType(str, Enum):
    CALLS = "calls"
    CALLED_BY = "called_by"
    INHERITS_FROM = "inherits_from"
    IMPLEMENTS = "implements"
    DEPENDS_ON = "depends_on"
    IMPORTS = "imports"
    CONTAINS = "contains"

@dataclass
class Relationship:
    """Represents a connection between two code entities."""
    target_id: str
    relationship_type: RelationshipType
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodeEntity:
    """Base class for all PEP code representations."""
    name: str
    # Stable identifier, generated using uuid if not provided
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    location: Optional[SourceLocation] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)

    def add_relationship(self, target_id: str, rel_type: RelationshipType, metadata: Optional[Dict[str, Any]] = None):
        self.relationships.append(Relationship(
            target_id=target_id,
            relationship_type=rel_type,
            metadata=metadata or {}
        ))

@dataclass
class Import(CodeEntity):
    """Represents an import statement."""
    module: str = ""
    alias: Optional[str] = None

@dataclass
class Variable(CodeEntity):
    """Represents a variable declaration (global, class-level, etc.)."""
    type_hint: Optional[str] = None
    value: Optional[str] = None

@dataclass
class Function(CodeEntity):
    """Represents a function or method."""
    return_type: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    is_async: bool = False
    is_method: bool = False

@dataclass
class Class(CodeEntity):
    """Represents a class definition."""
    base_classes: List[str] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    variables: List[Variable] = field(default_factory=list)

@dataclass
class File(CodeEntity):
    """Represents a single source code file."""
    path: str = ""
    classes: List[Class] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    variables: List[Variable] = field(default_factory=list)
    imports: List[Import] = field(default_factory=list)

@dataclass
class Repository(CodeEntity):
    """Represents the top-level repository or module structure."""
    url: Optional[str] = None
    branch: Optional[str] = None
    files: List[File] = field(default_factory=list)
    
    def get_file(self, path: str) -> Optional[File]:
        for f in self.files:
            if f.path == path:
                return f
        return None
