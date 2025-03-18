from typing import List, Optional
from pydantic import BaseModel

class TextInput(BaseModel):
    """
    A Pydantic model for text input.

    Attributes:
        text (str): The text to be processed.
    """
    text: str

class ImageSearchResult(BaseModel):
    """
    A Pydantic model for representing an image search result.

    Attributes:
        id (str): The identifier of the image.
        score (float): The similarity score of the image.
    """
    id: str
    score: float

class Product(BaseModel):
    """
    A Pydantic model for representing a product.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        description (str): A description of the product.
        material (Optional[str]): The material of the product.
        rating (Optional[float]): The rating of the product.
        images (List[str]): A list of image URLs associated with the product.
        code (Optional[str]): The product code.
        brand_id (Optional[int]): The identifier of the brand.
        brand_name (Optional[str]): The name of the brand.
        category_id (Optional[int]): The identifier of the category.
        category_name (Optional[str]): The name of the category.
        gender_id (Optional[int]): The identifier of the gender.
        gender_name (Optional[str]): The name of the gender.
        shop_id (Optional[int]): The identifier of the shop.
        shop_name (Optional[str]): The name of the shop.
        link (Optional[str]): A URL link to the product.
        status (Optional[str]): The status of the product.
        colors (Optional[List[str]]): A list of colors associated with the product.
        sizes (Optional[List[str]]): A list of sizes available for the product.
        region (Optional[str]): The region where the product is available.
        currency (Optional[str]): The currency in which the product is priced.
        current_price (Optional[float]): The current price of the product.
        old_price (Optional[float]): The old price of the product.
        off_percent (Optional[int]): The percentage off the original price.
        update_date (Optional[str]): The date when the product information was last updated.
    """
    id: int
    name: str
    description: str
    material: Optional[str]
    rating: Optional[float]
    images: List[str]
    code: Optional[str]
    brand_id: Optional[int]
    brand_name: Optional[str]
    category_id: Optional[int]
    category_name: Optional[str]
    gender_id: Optional[int]
    gender_name: Optional[str]
    shop_id: Optional[int]
    shop_name: Optional[str]
    link: Optional[str]
    status: Optional[str]
    colors: Optional[List[str]]
    sizes: Optional[List[str]]
    region: Optional[str]
    currency: Optional[str]
    current_price: Optional[float]
    old_price: Optional[float]
    off_percent: Optional[int]
    update_date: Optional[str]

class ProductSearchResponse(BaseModel):
    """
    A Pydantic model for representing a product search response.

    Attributes:
        hits (List[Product]): A list of products that match the search query.
        limit (int): The maximum number of products to return.
        offset (int): The number of products to skip before starting to return results.
    """
    hits: List[Product]
    limit: int
    offset: int

class SearchQuery(BaseModel):
    """
    A Pydantic model for representing a search query.

    Attributes:
        query (str): The search query text.
        limit (Optional[int]): The maximum number of results to return (default is 10).
        offset (Optional[int]): The number of results to skip before starting to return results (default is 0).
        filter (Optional[List[str]]): A list of filters to apply to the search.
        sort (Optional[List[str]]): A list of sorting criteria for the search results.
    """
    query: str
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    filter: Optional[List[str]] = []
    sort: Optional[List[str]] = []
