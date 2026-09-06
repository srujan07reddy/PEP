from typing import Dict, Any, List
from core.framework.models.knowledge_graph import KnowledgeGraph
import os
import sys

# Ensure plugin framework is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from core.framework.plugins.plugin_manager import PluginManager

class QualityEngine:
    """
    Analyzes code quality metrics based on AST properties stored in the Graph,
    and leverages AI Review adapters if available.
    """
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        self.plugin_manager = PluginManager()
        
        # Load adapters
        adapters_dir = os.path.join(self.workspace_root, "registry", "adapters")
        self.plugin_manager.load_plugins(adapters_dir)
        
    def analyze(self, kg: KnowledgeGraph) -> List[Dict[str, Any]]:
        """
        Executes code quality checks.
        """
        findings = []
        
        # 1. Base Static Checks
        for node in kg.pep_graph.nodes.values():
            if node.type == "function":
                # Assuming properties might have 'length' or we just check naming convention for now
                if len(node.name) < 3:
                    findings.append({
                        "engine": "QualityEngine",
                        "severity": "low",
                        "message": f"Function name '{node.name}' is too short, indicating poor quality.",
                        "node_id": node.id
                    })
                    
        # 2. Dynamic AI Review (via multiple AI adapters)
        ai_reviewers = self.plugin_manager.get_all_adapters("ai_code_review")
        for reviewer in ai_reviewers:
            # We would normally grab the source code from the node properties or file system.
            # Here we simulate finding a file to review.
            mock_code = "def f():\n    pass\n"
            
            # Use a safe fallback in case request_review fails
            try:
                ai_findings = reviewer.request_review(mock_code, "example_file.py")
            except Exception:
                ai_findings = []
            
            for finding in ai_findings:
                findings.append({
                    "engine": f"QualityEngine ({reviewer.get_name()})",
                    "severity": finding.get("severity", "medium"),
                    "message": finding.get("message", ""),
                    "suggestion": finding.get("suggestion", ""),
                    "node_id": "example_file.py"
                })
                
        return findings
