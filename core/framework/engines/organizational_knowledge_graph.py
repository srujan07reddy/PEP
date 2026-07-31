from typing import List, Dict, Any
from ..models.organization import OrganizationKnowledgeModel, OrganizationNode, OrganizationEdge

class OrganizationalKnowledgeGraph:
    """
    Compiles everything into a master graph database.
    Nodes: Organization, Department, Role, Workflow, Policy, ERP Module, etc.
    Edges: Reports To, Approves, Uses, Depends On, etc.
    """
    def __init__(self, okm: OrganizationKnowledgeModel):
        self.okm = okm
        self.nodes: Dict[str, OrganizationNode] = {n.id: n for n in okm.nodes}
        self.edges: List[OrganizationEdge] = okm.edges
        
    def query_nodes_by_type(self, node_type: str) -> List[OrganizationNode]:
        return [node for node in self.nodes.values() if node.type == node_type]
