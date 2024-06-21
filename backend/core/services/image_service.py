from core.repositories.image_repository import ImageRepository
from core.schemas import ImageOutput

class ImageService:
    def __init__(self):
        self.repository = ImageRepository()

    async def process_image(self, image_data: bytes) -> ImageOutput:
        processed_image = await self.repository.process_image(image_data)
        return ImageOutput(result=processed_image)
