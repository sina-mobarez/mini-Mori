from repositories.image_repository import ImageRepository
from utils import clip_model_wrapper

class ImageService:
    def __init__(self):
        self.repository = ImageRepository()

    async def process_image(self, image_data: bytes) -> dict:
        processed_image = await self.repository.process_image(image_data)
        return {"result": processed_image}

    async def search_similar_images(self, text: str, limit=5) -> list:
        embedding = clip_model_wrapper.generate_text_embedding(text)
        results = await self.repository.search_similar_images(embedding, limit)
        return [{"id": result.id, "score": result.score} for result in results]
