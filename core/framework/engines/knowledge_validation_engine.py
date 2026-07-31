from typing import List, Dict, Any, Set
from ..models.organization import OrganizationKnowledgeModel
from .organizational_knowledge_graph import OrganizationalKnowledgeGraph

class KnowledgeValidationEngine:
    """
    Validates organizational knowledge.
    Uses DFS algorithm to detect cyclic dependencies (e.g., circular approvals)
    and checks for orphaned nodes (e.g., roles without departments).
    """
    def __init__(self):
        pass
        
    def validate(self, okm: OrganizationKnowledgeModel) -> List[Dict[str, Any]]:
        issues = []
        
        okg = OrganizationalKnowledgeGraph(okm)
        
        # 1. Orphan Detection
        for node in okg.nodes.values():
            if node.type == "Role":
                has_dept = False
                for edge in okg.edges:
                    if edge.source_id == node.id and edge.relationship == "Belongs To":
                        has_dept = True
                        break
                if not has_dept:
                    issues.append({"type": "orphaned_role", "severity": "medium", "message": f"Role '{node.name}' ({node.id}) does not belong to any department."})
                    
        # 2. Cycle Detection using DFS (specifically for 'Reports To' and 'Requires Approval From')
        visited = set()
        recursion_stack = set()
        
        # Build adjacency list for directional relationships that shouldn't cycle
        adj_list = {n_id: [] for n_id in okg.nodes.keys()}
        for edge in okg.edges:
            if edge.relationship in ["Reports To"] or edge.relationship.startswith("Requires Approval From"):
                adj_list[edge.source_id].append(edge.target_id)
                
        def dfs_cycle_detect(node_id: str, path: List[str]) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)
            
            for neighbor in adj_list.get(node_id, []):
                if neighbor not in visited:
                    if dfs_cycle_detect(neighbor, path + [neighbor]):
                        return True
                elif neighbor in recursion_stack:
                    path.append(neighbor) # complete the cycle for reporting
                    issues.append({
                        "type": "circular_dependency",
                        "severity": "high",
                        "message": f"Circular dependency detected in graph: {' -> '.join(path)}"
                    })
                    return True
                    
            recursion_stack.remove(node_id)
            return False

        for node_id in adj_list.keys():
            if node_id not in visited:
                dfs_cycle_detect(node_id, [node_id])
                
        return issues
