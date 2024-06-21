from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from core.config import settings
from core.utils import generate_text_embedding

class TextRepository:
    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection_name = "texts"
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={"size": 512, "distance": "Cosine"}
        )

    async def process_text(self, text: str) -> str:
        # Generate text embedding
        embedding = generate_text_embedding(text)
        point = PointStruct(id=1, vector=embedding, payload={"text": text})
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return text.upper()
