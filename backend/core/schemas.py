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
