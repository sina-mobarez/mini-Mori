from fastapi import FastAPI, Query
from core.schemas import ProductSearchResponse, TextInput, ImageSearchResult
from core.services.image_service import ImageService
from core.meilisearch_client import client

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



@app.get("/products", response_model=ProductSearchResponse)
async def search_products(
    q: str = Query(None, description="Search query"),
    limit: int = Query(10, description="Number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    sort: str = Query(None, description="Sort by a specific attribute"),
    filter: str = Query(None, description="Filter by a specific attribute")
):
    """
    Endpoint to search products with support for pagination, filtering, and sorting.

    :param q: Search query.
    :param limit: Number of results to return.
    :param offset: Number of results to skip.
    :param sort: Sort by a specific attribute.
    :param filter: Filter by a specific attribute.
    :return: Paginated list of products.
    """
    search_params = {
        "q": q,
        "limit": limit,
        "offset": offset,
        "sort": [sort] if sort else None,
        "filter": [filter] if filter else None
    }
    result = client.index('products').search(**search_params)
    return ProductSearchResponse(
        hits=result['hits'],
        total=result['nbHits'],
        limit=limit,
        offset=offset
    )