import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.framework.models.knowledge_graph import KnowledgeGraph
from core.framework.models.pep_graph import PEPGraph, Node, Edge
from core.framework.engines.engineering_decision_board import EngineeringDecisionBoard
from core.framework.engines.engineering_maturity_engine import EngineeringMaturityEngine

class TestEngineeringIntelligence(unittest.TestCase):
    
    def setUp(self):
        maturity = EngineeringMaturityEngine(okg=None)
        self.board = EngineeringDecisionBoard(maturity_engine=maturity)

    def test_evaluate_knowledge_graph(self):
        # Create a mock KnowledgeGraph
        kg = KnowledgeGraph()
        pep_graph = PEPGraph()
        
        # 1. Requirement Engine failure: A Database class exists but no requirements mapped 
        # (based on our simple heuristic)
        db_node = Node(id="UserDatabase", type="class", properties={})
        pep_graph.add_node(db_node)
        
        # 2. Quality Engine failure: Short function name
        func_node = Node(id="do", type="function", properties={})
        pep_graph.add_node(func_node)
        
        # 3. Architecture Engine failure: Controller calling Controller directly
        c1 = Node(id="UserController", type="class", properties={})
        c2 = Node(id="BillingController", type="class", properties={})
        pep_graph.add_node(c1)
        pep_graph.add_node(c2)
        pep_graph.add_edge(Edge(source="UserController", target="BillingController", relation="calls"))
        
        # 4. Security Engine failure: calling eval
        eval_node = Node(id="eval", type="function", properties={})
        pep_graph.add_node(eval_node)
        pep_graph.add_edge(Edge(source="UserController", target="eval", relation="calls"))
        
        kg.merge_pep_graph(pep_graph)
        
        # Run through board
        report = self.board.evaluate_knowledge_graph(kg)
        
        # Validate finding counts
        summary = report["findings_summary"]
        self.assertTrue(len(summary["requirements"]) > 0, "Requirement Engine should find DB issue")
        self.assertTrue(len(summary["architecture"]) > 0, "Architecture Engine should find controller coupling")
        self.assertTrue(len(summary["quality"]) > 0, "Quality Engine should find short func name")
        self.assertTrue(len(summary["security"]) > 0, "Security Engine should find eval call")
        
        # Validate risk score is correct (medium=5, high=15, critical=25 -> 45)
        self.assertEqual(report["overall_risk_score"], 45)
        self.assertEqual(report["status"], "HEALTHY")

if __name__ == "__main__":
    unittest.main()
