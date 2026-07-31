from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class OrganizationNode(BaseModel):
    id: str
    type: str # Department, Role, Policy, Process, Module, Person
    name: str
    attributes: Dict[str, str] = {}

class OrganizationEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str # ReportsTo, Approves, DependsOn, BelongsTo, Uses, Owns, ParticipatesIn, Triggers, References

class Department(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None

class Role(BaseModel):
    id: str
    name: str
    department_id: Optional[str] = None
    reports_to_role_id: Optional[str] = None

class Workflow(BaseModel):
    id: str
    name: str
    trigger: str
    approval_chain_ids: List[str] = [] # list of Role IDs
    associated_policies: List[str] = [] # list of Policy IDs
    
class Policy(BaseModel):
    id: str
    name: str
    description: str
    compliance_mappings: List[str] = []

class OrganizationKnowledgeModel(BaseModel):
    name: str
    type: str
    industry: str
    country: str
    
    nodes: List[OrganizationNode] = []
    edges: List[OrganizationEdge] = []
    
    departments: List[Department] = []
    roles: List[Role] = []
    workflows: List[Workflow] = []
    policies: List[Policy] = []
