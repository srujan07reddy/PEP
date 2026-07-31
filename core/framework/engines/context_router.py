from typing import List, Dict, Any
from .organizational_knowledge_graph import OrganizationalKnowledgeGraph
from ..models.organization import OrganizationNode

class ContextRouter:
    """
    Instead of exposing the entire Knowledge Graph to every agent,
    routes only relevant context (sub-graphs).
    """
    def __init__(self, okg: OrganizationalKnowledgeGraph):
        self.okg = okg
        
    def route_to_workflow_agent(self) -> List[OrganizationNode]:
        return self.okg.query_nodes_by_type("Workflow")
        
    def route_to_policy_agent(self) -> List[OrganizationNode]:
        return self.okg.query_nodes_by_type("Policy")
        
    def route_to_hierarchy_agent(self) -> List[OrganizationNode]:
        deps = self.okg.query_nodes_by_type("Department")
        roles = self.okg.query_nodes_by_type("Role")
        return deps + roles
