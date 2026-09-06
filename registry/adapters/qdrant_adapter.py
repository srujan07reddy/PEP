from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

class QdrantAdapter:
    """
    Adapter to interact with Qdrant for vector-based semantic search.
    """
    def __init__(self, host: str = "localhost", port: int = 6333, vector_size: int = 384):
        self.client = QdrantClient(host=host, port=port)
        self.vector_size = vector_size

    def ensure_collection(self, collection_name: str):
        """Creates a collection if it doesn't already exist."""
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

    def upsert_point(self, collection_name: str, vector: List[float], payload: Dict[str, Any], point_id: Optional[str] = None):
        """Inserts or updates a vector point in the collection."""
        if point_id is None:
            point_id = str(uuid.uuid4())
            
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        )
        self.client.upsert(
            collection_name=collection_name,
            points=[point]
        )
        return point_id

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Searches for similar vectors in the collection."""
        hits = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        results = []
        for hit in hits:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            })
        return results
