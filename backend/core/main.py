from fastapi import FastAPI
from core.schemas import ProductSearchResponse, SearchQuery, TextInput, ImageSearchResult
from core.services.image_service import ImageService
from core.services.meilisearch_service import MeiliSearchService

app = FastAPI()

image_service = ImageService()
meili_search_service = MeiliSearchService()

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

@app.post("/search-products", response_model=ProductSearchResponse)
async def search_products(search_query: SearchQuery):
    """
    Endpoint to search for products using MeiliSearch.

    Args:
        search_query (SearchQuery): The search query parameters including query text, limit, offset, filters, and sorting criteria.

    Returns:
        ProductSearchResponse: A response containing the search results.
    """
    results = await meili_search_service.search_products(
        query=search_query.query,
        limit=search_query.limit,
        offset=search_query.offset,
        filter=search_query.filter,
        sort=search_query.sort
    )
    return results
