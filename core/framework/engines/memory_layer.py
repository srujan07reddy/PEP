from typing import Dict, Any, List
import sys
import os
import random

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from core.framework.models.pep_graph import PEPGraph
from core.framework.models.knowledge_graph import KnowledgeGraph
from registry.adapters.neo4j_adapter import Neo4jAdapter
from registry.adapters.qdrant_adapter import QdrantAdapter

class MemoryLayer:
    """
    Core orchestrator that takes structured Code Understanding and Domain Knowledge
    and flushes them into Neo4j (structural/relational memory) and Qdrant (semantic memory).
    """
    
    def __init__(self):
        self.neo4j = Neo4jAdapter()
        self.qdrant = QdrantAdapter()
        
        # Ensure collections exist in Qdrant
        self.qdrant.ensure_collection("code_snippets")
        self.qdrant.ensure_collection("policies")
        self.qdrant.ensure_collection("requirements")

    def _mock_embedding(self, text: str) -> List[float]:
        """
        Generates a mock embedding of size 384 for a given text.
        In production, this would call an LLM or sentence-transformer model.
        """
        random.seed(hash(text))
        return [random.uniform(-1, 1) for _ in range(384)]

    def ingest_knowledge_graph(self, kg: KnowledgeGraph):
        """
        Ingests a KnowledgeGraph into the memory layer.
        """
        # 1. Store Graph topology in Neo4j
        for node in kg.pep_graph.nodes.values():
            self.neo4j.merge_node(
                label=node.type.capitalize(), 
                node_id=node.id, 
                properties=node.properties
            )
            
            # 2. Store textual representation in Qdrant for semantic search
            # If the node has source code or docstrings, embed it
            text_to_embed = str(node.properties)
            vector = self._mock_embedding(text_to_embed)
            
            payload = {
                "id": node.id,
                "type": node.type,
                "properties": node.properties
            }
            
            # Assuming nodes from code understanding go to "code_snippets"
            self.qdrant.upsert_point(
                collection_name="code_snippets",
                vector=vector,
                payload=payload,
                # UUID generation is handled by the adapter if point_id is None, but let's pass a determinist UUID or None
                point_id=None
            )

        for edge in kg.pep_graph.edges:
            self.neo4j.merge_edge(
                source_id=edge.source,
                target_id=edge.target,
                rel_type=edge.relation.upper(),
                properties=edge.properties
            )

    def ingest_policy(self, policy_id: str, policy_text: str, metadata: Dict[str, Any] = None):
        """
        Ingests a policy into the memory layer.
        """
        # Store structurally in Neo4j
        props = metadata or {}
        props["text"] = policy_text
        self.neo4j.merge_node("Policy", policy_id, props)
        
        # Store semantically in Qdrant
        vector = self._mock_embedding(policy_text)
        self.qdrant.upsert_point(
            collection_name="policies",
            vector=vector,
            payload={"policy_id": policy_id, "text": policy_text, **props}
        )

    def close(self):
        """Cleans up resources."""
        self.neo4j.close()
