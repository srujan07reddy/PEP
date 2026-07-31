from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class GovernanceMode(str, Enum):
    ADVISORY = "advisory"
    WARNING = "warning"
    BLOCKING = "blocking"

class Agent(BaseModel):
    id: str = Field(..., description="Unique UUID for the agent instance")
    name: str
    version: str
    governance_domain: str
    mode: GovernanceMode
    
    can_generate: bool = False
    can_review: bool = True
    can_approve: bool = False
    can_reject: bool = False
    can_deploy: bool = False
    
    dependencies: List[str] = Field(default_factory=list)
