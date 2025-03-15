from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import ProductSearchResponse, SearchQuery, TextInput, ImageSearchResult
from core.services.image_service import ImageService
from core.services.product_service import ProductService

app = FastAPI()

# CORS configuration
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

image_service = ImageService()
product_service = ProductService()

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
    results = await product_service.search_products(
        query=search_query.query,
        limit=search_query.limit,
        offset=search_query.offset,
        filter=search_query.filter,
        sort=search_query.sort
    )
    return results


@app.get("/search-products-by-ids", response_model=List[dict])
async def search_products_by_ids(ids: List[int] = Query(...)):
    """
    Endpoint to search for products based on a list of IDs.

    Args:
        ids (List[int]): List of product IDs.

    Returns:
        ProductSearchResponse: A list of products matching the provided IDs.
    """
    results = product_service.search_products_by_ids(ids)
    return results


@app.get("/search-products-by-keywords", response_model=ProductSearchResponse)
async def search_products_by_keywords(keywords: list = Query(...)):
    """
    Endpoint to search for products based on a list of keywords.

    Args:
        keywords (list): List of keywords to search for in product names, descriptions, etc.

    Returns:
        ProductSearchResponse: A list of products matching the provided keywords.
    """
    results = await product_service.search_products_by_keywords(keywords)
    return results