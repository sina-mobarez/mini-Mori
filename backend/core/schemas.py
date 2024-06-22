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
    hits: List[Product]
    total: int
    limit: int
    offset: int