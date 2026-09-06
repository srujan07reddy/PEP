import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.framework.engines.memory_layer import MemoryLayer
from core.framework.models.knowledge_graph import KnowledgeGraph
from core.framework.models.pep_graph import PEPGraph, Node, Edge

class TestMemoryLayer(unittest.TestCase):
    
    @patch('core.framework.engines.memory_layer.QdrantAdapter')
    @patch('core.framework.engines.memory_layer.Neo4jAdapter')
    def setUp(self, MockNeo4j, MockQdrant):
        self.mock_neo4j = MockNeo4j.return_value
        self.mock_qdrant = MockQdrant.return_value
        
        self.memory = MemoryLayer()

    def test_ingest_knowledge_graph(self):
        # Create a mock KnowledgeGraph
        kg = KnowledgeGraph()
        pep_graph = PEPGraph()
        
        node = Node(id="TestClass", type="class", properties={"name": "TestClass"})
        edge = Edge(source="func1", target="func2", relation="calls")
        
        pep_graph.add_node(node)
        pep_graph.add_edge(edge)
        kg.merge_pep_graph(pep_graph)
        
        # Ingest
        self.memory.ingest_knowledge_graph(kg)
        
        # Verify Neo4j calls
        self.mock_neo4j.merge_node.assert_called_with(
            label="Class",
            node_id="TestClass",
            properties={"name": "TestClass"}
        )
        self.mock_neo4j.merge_edge.assert_called_with(
            source_id="func1",
            target_id="func2",
            rel_type="CALLS",
            properties={}
        )
        
        # Verify Qdrant calls (should upsert one point for the node)
        self.assertEqual(self.mock_qdrant.upsert_point.call_count, 1)
        args, kwargs = self.mock_qdrant.upsert_point.call_args
        self.assertEqual(kwargs["collection_name"], "code_snippets")
        self.assertEqual(kwargs["payload"]["id"], "TestClass")

    def test_ingest_policy(self):
        policy_id = "POL-001"
        policy_text = "All modules must be typed."
        
        self.memory.ingest_policy(policy_id, policy_text)
        
        # Verify Neo4j call
        self.mock_neo4j.merge_node.assert_called_with(
            "Policy",
            "POL-001",
            {"text": "All modules must be typed."}
        )
        
        # Verify Qdrant call
        self.assertEqual(self.mock_qdrant.upsert_point.call_count, 1)
        args, kwargs = self.mock_qdrant.upsert_point.call_args
        self.assertEqual(kwargs["collection_name"], "policies")
        self.assertEqual(kwargs["payload"]["policy_id"], "POL-001")

if __name__ == "__main__":
    unittest.main()
