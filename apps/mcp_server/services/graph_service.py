from typing import Dict, Any
from .contracts import BaseService

class GraphService(BaseService):
    def generate_dependency_graph(self, domain_id: str) -> Dict[str, Any]:
        """
        Generates the unified Knowledge Graph using KnowledgeGraphBuilder.
        """
        context = self.app.analysis.get_or_create_context(domain_id)
        
        try:
            from core.framework.engines.knowledge_graph_builder import KnowledgeGraphBuilder
            
            # The builder performs its own AST parsing (tree-sitter) independent of ArchitectureEngine.
            builder = KnowledgeGraphBuilder()
            kg = builder.build(str(self.workspace_root))
            
            context.code = kg
            
            return {
                "status": "success",
                "data": {
                    "domain_id": domain_id,
                    "nodes": len(kg.pep_graph.nodes),
                    "edges": len(kg.pep_graph.edges),
                    "semantic_symbols": len(getattr(kg, "symbols", [])) # Changed from kg.semantic_symbols based on knowledge_graph definition
                }
            }
            
        except Exception as e:
            return {
                "status": "partial_success" if (context.business.organization or context.analyses.architecture) else "failed",
                "errors": [{"code": "GRAPH_GENERATION_FAILED", "message": str(e)}]
            }
