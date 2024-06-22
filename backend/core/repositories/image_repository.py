from qdrant_client import QdrantClient
from config import settings

class ImageRepository:
    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection_name = "images"
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 512, "distance": "Cosine"}
            )

    async def upsert_images(self, points):
        self.client.upsert(collection_name=self.collection_name, points=points)

    async def search_similar_images(self, embedding, limit=5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=limit,
        )
        return results

