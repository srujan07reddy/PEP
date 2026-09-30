from typing import List, Dict, Any
from core.models.evidence import Evidence
from core.models.knowledge import KnowledgeGraph, KnowledgeNode

class KnowledgeCompiler:
    """
    The PEP Knowledge Compiler.
    
    Ingests disparate Evidence nodes from both Code Models and Text Models, 
    and compiles them into a connected Knowledge Graph by determining 
    cross-domain relationships.
    """
    
    def __init__(self):
        self.graph = KnowledgeGraph()
        
    def ingest(self, evidence_list: List[Evidence]) -> None:
        """Ingests independent facts into the compiler."""
        for evidence in evidence_list:
            node = KnowledgeNode(
                evidence=evidence, 
                node_type=evidence.evidence_type,
                id=evidence.id # Bind the node ID to the evidence ID for O(1) traversals
            )
            self.graph.add_node(node)
            
    def compile(self) -> KnowledgeGraph:
        """
        Executes linking heuristics, embedding proximity matches, and semantic 
        mapping to determine relationships between independently extracted facts.
        """
        nodes = list(self.graph.nodes.values())
        
        for i, source_node in enumerate(nodes):
            for target_node in nodes[i+1:]:
                # Route relationship checking based on node boundaries
                
                # Boundary 1: Policy/Requirement <---> Code Implementation
                is_policy_a = source_node.node_type in ["Requirement", "Policy", "Rule"]
                is_code_b = target_node.node_type in ["Function", "Class", "Variable"]
                
                is_code_a = source_node.node_type in ["Function", "Class", "Variable"]
                is_policy_b = target_node.node_type in ["Requirement", "Policy", "Rule"]
                
                if is_policy_a and is_code_b:
                    self._evaluate_implementation_link(source_node, target_node)
                elif is_code_a and is_policy_b:
                    self._evaluate_implementation_link(target_node, source_node)
                    
                # Boundary 2: Role <---> Requirement
                # self._evaluate_governance_link(source_node, target_node)
                
        return self.graph

    def _evaluate_implementation_link(self, policy_node: KnowledgeNode, code_node: KnowledgeNode):
        """
        Evaluates if a piece of code implements or violates a specific policy/requirement.
        Uses heuristics or ML embeddings to bridge the vocabulary gap.
        """
        # Mocking the compiler intelligence logic:
        # Example: Policy says "requires DBA approval" for "database change"
        # Code says: function "deploy_database" in "deployment.py"
        
        policy_payload = str(policy_node.evidence.payload).lower()
        code_payload = str(code_node.evidence.payload).lower()
        code_source = str(code_node.evidence.source).lower()
        
        # Simple keyword/context heuristic simulating embedding similarity
        if "database" in policy_payload and ("database" in code_payload or "database" in code_source):
            if "deploy" in code_payload or "deploy" in code_source:
                # The compiler infers the code implements the policy boundary
                self.graph.add_edge(
                    source_id=policy_node.id, 
                    target_id=code_node.id, 
                    relation="implemented_by",
                    weight=0.88,
                    metadata={"reason": "Semantic similarity match between policy payload and code implementation"}
                )
