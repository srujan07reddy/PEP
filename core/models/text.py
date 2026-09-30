from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import uuid

@dataclass
class TextLocation:
    """Represents a specific location within a text document."""
    start_char: int
    end_char: int
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    paragraph_index: Optional[int] = None

@dataclass
class TextElement:
    """Base class for all PEP organizational language representations."""
    text_value: str
    source_document: str
    evidence: str
    confidence: float
    location: Optional[TextLocation] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Entity(TextElement):
    """Represents a named entity or domain concept (e.g., 'User', 'Payment Gateway')."""
    entity_type: str = "generic"

@dataclass
class Relation(TextElement):
    """Represents a semantic relationship between entities."""
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: str = ""

@dataclass
class Requirement(TextElement):
    """Represents a functional or non-functional requirement."""
    priority: str = "medium"
    status: str = "proposed"

@dataclass
class Rule(TextElement):
    """Represents a business logic rule or condition."""
    strictness: str = "mandatory"

@dataclass
class Policy(TextElement):
    """Represents an organizational, compliance, or security policy."""
    policy_domain: str = "general"

@dataclass
class Constraint(TextElement):
    """Represents a technical or business constraint limiting the system."""
    constraint_type: str = "technical"

@dataclass
class Event(TextElement):
    """Represents an action, trigger, or system event."""
    trigger_condition: Optional[str] = None

@dataclass
class Document:
    """Represents a processed natural language document containing organizational knowledge."""
    title: str
    source_path: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    entities: List[Entity] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    requirements: List[Requirement] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    policies: List[Policy] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)
