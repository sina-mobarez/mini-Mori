from PIL import Image
import io
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from core.config import settings
from core.utils import generate_image_embedding

class ImageRepository:
    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection_name = "images"
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={"size": 512, "distance": "Cosine"}
        )

    async def process_image(self, image_data: bytes) -> str:
        image = Image.open(io.BytesIO(image_data))
        # Generate image embedding
        embedding = generate_image_embedding(image)
        point = PointStruct(id=1, vector=embedding, payload={"size": image.size})
        self.client.upsert(collection_name=self.collection_name, points=[point])
        width, height = image.size
        return f"Image size: {width}x{height}"

