from qdrant_client import QdrantClient
from core.config import settings

class ImageRepository:
    """
    Repository class for handling interactions with the Qdrant image database.

    Attributes:
        client (QdrantClient): The Qdrant client for interacting with the database.
        collection_name (str): The name of the collection in the Qdrant database.
    """

    def __init__(self):
        """
        Initializes the ImageRepository with a Qdrant client and ensures the collection exists.
        """
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection_name = "images"
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensures that the image collection exists in the Qdrant database. If it does not exist, it creates the collection.
        """
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 512, "distance": "Cosine"}
            )

    async def upsert_images(self, points: list):
        """
        Upserts (inserts or updates) image points into the Qdrant database.

        Args:
            points (list): A list of points to upsert into the database.
        """
        self.client.upsert(collection_name=self.collection_name, points=points)

    async def search_similar_images(self, embedding: list, limit: int = 5) -> list:
        """
        Searches for images similar to the given embedding.

        Args:
            embedding (list): The embedding vector to search for similar images.
            limit (int, optional): The maximum number of similar images to return. Defaults to 5.

        Returns:
            list: A list of search results containing similar images.
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=limit,
        )
        return results
