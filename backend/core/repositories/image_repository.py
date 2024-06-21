from PIL import Image
import io

class ImageRepository:
    async def process_image(self, image_data: bytes) -> str:
        image = Image.open(io.BytesIO(image_data))
        # Example processing: get image size
        width, height = image.size
        return f"Image size: {width}x{height}"
