from typing import List, Dict, Any
from ..models.organization import OrganizationKnowledgeModel, OrganizationNode, OrganizationEdge

class KnowledgeGraph:
    """
    Converts organizational information into a traversable graph.
    """
    def __init__(self, okm: OrganizationKnowledgeModel):
        self.okm = okm
        self.nodes: Dict[str, OrganizationNode] = {n.id: n for n in okm.nodes}
        self.edges: List[OrganizationEdge] = okm.edges
        
    def get_related_nodes(self, node_id: str, relationship: str = None) -> List[OrganizationNode]:
        related = []
        for edge in self.edges:
            if edge.source_id == node_id and (relationship is None or edge.relationship == relationship):
                if edge.target_id in self.nodes:
                    related.append(self.nodes[edge.target_id])
        return related
