from typing import Dict, Any, List
from ...models.organization import OrganizationNode, OrganizationEdge

class RelationshipExtractionEngine:
    """
    Builds the graph edges by inspecting attributes of OrganizationNodes
    (e.g., 'reports_to', 'approver_id', 'department_id').
    """
    def extract_relationships(self, nodes: List[OrganizationNode]) -> List[OrganizationEdge]:
        edges = []
        node_ids = {n.id for n in nodes}
        
        for node in nodes:
            # 1. 'reports_to' relationship in Roles
            if node.type == "Role" and "reports_to" in node.attributes:
                target_id = node.attributes["reports_to"]
                if target_id in node_ids:
                    edges.append(OrganizationEdge(source_id=node.id, target_id=target_id, relationship="Reports To"))
                    
            # 2. 'department_id' relationship in Roles
            if node.type == "Role" and "department_id" in node.attributes:
                target_id = node.attributes["department_id"]
                if target_id in node_ids:
                    edges.append(OrganizationEdge(source_id=node.id, target_id=target_id, relationship="Belongs To"))
                    
            # 3. 'approval_chain' in Workflows
            if node.type == "Workflow" and "approval_chain" in node.attributes:
                approvers = node.attributes["approval_chain"]
                for i, target_id in enumerate(approvers):
                    if target_id in node_ids:
                        edges.append(OrganizationEdge(source_id=node.id, target_id=target_id, relationship=f"Requires Approval From (Level {i+1})"))
                        
            # 4. 'depends_on' relationship in any entity
            if "depends_on" in node.attributes:
                dependencies = node.attributes["depends_on"]
                if isinstance(dependencies, list):
                    for target_id in dependencies:
                        if target_id in node_ids:
                            edges.append(OrganizationEdge(source_id=node.id, target_id=target_id, relationship="Depends On"))

        return edges
