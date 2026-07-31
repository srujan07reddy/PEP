from typing import Dict, Any
from .organization_intelligence_layer import OrganizationIntelligenceLayer
from .knowledge_graph import KnowledgeGraph

class ContextEngine:
    """
    Aggregates Organization Context, Business Context, Workflow Context,
    and Policy Context before any recommendation is generated.
    """
    def __init__(self, oil: OrganizationIntelligenceLayer):
        self.oil = oil
        
    def get_agent_context(self, org_id: str) -> Dict[str, Any]:
        okm = self.oil.load_organization_knowledge(org_id)
        graph = KnowledgeGraph(okm)
        
        return {
            "organization": okm,
            "graph": graph,
            "policies_count": len(okm.policies),
            "workflows_count": len(okm.workflows)
        }
