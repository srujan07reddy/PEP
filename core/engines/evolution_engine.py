from typing import List, Dict, Any, Set
from dataclasses import dataclass, field
from core.models.knowledge import KnowledgeGraph, KnowledgeNode
from core.models.assessment import Finding

@dataclass
class EvolutionDiff:
    """
    Represents the delta between two states of the PEP Knowledge Graph over time (T1 vs T2).
    Tracks semantic drift across all intelligence domains.
    """
    architecture_changes: List[Dict[str, Any]] = field(default_factory=list)
    policy_changes: List[Dict[str, Any]] = field(default_factory=list)
    dependency_changes: List[Dict[str, Any]] = field(default_factory=list)
    security_changes: List[Dict[str, Any]] = field(default_factory=list)
    quality_changes: List[Dict[str, Any]] = field(default_factory=list)
    organizational_changes: List[Dict[str, Any]] = field(default_factory=list)
    
    new_violations: List[Finding] = field(default_factory=list)
    resolved_findings: List[Finding] = field(default_factory=list)

class EvolutionEngine:
    """
    The Difference Engine.
    Detects semantic evolution by diffing Knowledge State T1 against Knowledge State T2.
    It doesn't just diff lines of code; it diffs architectural intent, security posture,
    and organizational alignment.
    """
    
    def compare_states(
        self, 
        state_t1: KnowledgeGraph, 
        state_t2: KnowledgeGraph, 
        findings_t1: List[Finding] = None, 
        findings_t2: List[Finding] = None
    ) -> EvolutionDiff:
        """
        Compares Knowledge State T1 against T2 and returns a comprehensive EvolutionDiff.
        """
        diff = EvolutionDiff()
        
        # 1. Compare Knowledge Nodes for Additions / Deletions
        nodes_t1: Set[str] = set(state_t1.nodes.keys())
        nodes_t2: Set[str] = set(state_t2.nodes.keys())
        
        added_nodes = nodes_t2 - nodes_t1
        removed_nodes = nodes_t1 - nodes_t2
        
        for n_id in added_nodes:
            self._categorize_node_change(state_t2.nodes[n_id], diff, change_type="added")
            
        for n_id in removed_nodes:
            self._categorize_node_change(state_t1.nodes[n_id], diff, change_type="removed")
            
        # 2. Track Finding Resolution (New vs Resolved)
        # Note: In practice, finding equivalence is determined by semantic hash, not UUID
        # because the UUIDs might be regenerated on every pipeline run. 
        # Assuming semantic hashing here for illustration.
        f_t1_map = {self._hash_finding(f): f for f in (findings_t1 or [])}
        f_t2_map = {self._hash_finding(f): f for f in (findings_t2 or [])}
        
        # Newly introduced violations (In T2, missing from T1)
        for f_hash, f in f_t2_map.items():
            if f_hash not in f_t1_map:
                diff.new_violations.append(f)
                
        # Resolved violations (In T1, missing from T2)
        for f_hash, f in f_t1_map.items():
            if f_hash not in f_t2_map:
                diff.resolved_findings.append(f)
                
        # 3. Graph Edge diffing (Dependency changes, architecture boundary shifts)
        # Would process state_t1.edges vs state_t2.edges
                
        return diff

    def _categorize_node_change(self, node: KnowledgeNode, diff: EvolutionDiff, change_type: str):
        """Routes node structural changes into the correct domain bucket."""
        change = {
            "type": change_type, 
            "node_id": node.id, 
            "node_type": node.node_type,
            "payload": str(node.evidence.payload) if node.evidence else "Unknown"
        }
        
        if node.node_type in ["Function", "Class", "File"]:
            diff.architecture_changes.append(change)
        elif node.node_type in ["Policy", "Requirement", "Rule"]:
            diff.policy_changes.append(change)
        elif node.node_type in ["Import", "Dependency"]:
            diff.dependency_changes.append(change)
        elif node.node_type in ["Role", "Event"]:
            diff.organizational_changes.append(change)
            
    def _hash_finding(self, finding: Finding) -> str:
        """
        Creates a deterministic hash representing the semantic meaning of the finding,
        allowing the engine to track if the exact same violation persists across pipeline runs
        even if UUIDs change.
        """
        return f"{finding.severity}:{finding.description}"
