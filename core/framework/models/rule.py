from pydantic import BaseModel, Field
from typing import Any, Dict
from enum import Enum

class RuleSeverity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"

class Rule(BaseModel):
    rule_id: str
    standard_domain: str
    description: str
    severity: RuleSeverity
    condition: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
