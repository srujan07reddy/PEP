from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase

class Neo4jAdapter:
    """
    Adapter to interact with a Neo4j database to store the PEP Graph.
    """
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def merge_node(self, label: str, node_id: str, properties: Dict[str, Any] = None):
        """Creates or updates a node with the given label, ID, and properties."""
        props = properties or {}
        # Ensure we always store the id
        props["id"] = node_id
        
        query = (
            f"MERGE (n:{label} {{id: $node_id}}) "
            f"SET n += $properties "
            f"RETURN n"
        )
        
        with self.driver.session() as session:
            session.run(query, node_id=node_id, properties=props)

    def merge_edge(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any] = None):
        """Creates or updates a relationship between two nodes."""
        props = properties or {}
        
        query = (
            f"MATCH (a {{id: $source_id}}) "
            f"MATCH (b {{id: $target_id}}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            f"SET r += $properties "
            f"RETURN r"
        )
        
        with self.driver.session() as session:
            session.run(query, source_id=source_id, target_id=target_id, properties=props)

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Executes a custom cypher query and returns the results."""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
