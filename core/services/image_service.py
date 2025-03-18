from repositories.image_repository import ImageRepository
from utils import clip_model_wrapper

class ImageService:
    """
    Service class for handling image-related operations, such as searching for similar images.

    Attributes:
        repository (ImageRepository): The repository for interacting with the image database.
    """

    def __init__(self):
        """
        Initializes the ImageService with an instance of ImageRepository.
        """
        self.repository = ImageRepository()

    async def search_similar_images(self, text: str, limit: int = 5) -> list:
        """
        Searches for images similar to the given text query.

        Args:
            text (str): The text query to search for similar images.
            limit (int, optional): The maximum number of similar images to return. Defaults to 5.

        Returns:
            list: A list of dictionaries containing the image IDs and their similarity scores.
        """
        embedding = clip_model_wrapper.generate_text_embedding(text)
        results = await self.repository.search_similar_images(embedding, limit)
        return [{"id": str(result['id']), "score": result['score']} for result in results]
