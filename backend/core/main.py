from fastapi import FastAPI
from core.schemas import TextInput, ImageSearchResult
from core.services.image_service import ImageService

app = FastAPI()

image_service = ImageService()

@app.post("/search-images", response_model=list[ImageSearchResult])
async def search_images(text_input: TextInput):
    """
    Endpoint to search for images similar to the given text input.

    Args:
        text_input (TextInput): The text input to search for similar images.

    Returns:
        list[ImageSearchResult]: A list of search results containing image IDs and similarity scores.
    """
    results = await image_service.search_similar_images(text_input.text)
    return results
