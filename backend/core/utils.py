import torch
import clip
from PIL import Image
import io
import aiohttp

class CLIPModelWrapper:
    """
    A wrapper class for OpenAI's CLIP model to generate text and image embeddings.

    Attributes:
        device (str): The device to run the model on ('cuda' if GPU is available, else 'cpu').
        model: The CLIP model loaded.
        preprocess: The preprocessing function for the CLIP model.
    """

    def __init__(self):
        """Initializes the CLIP model and sets the device for computation."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def generate_text_embedding(self, text: str) -> list:
        """
        Generates a text embedding for a given text string.

        Args:
            text (str): The input text to be embedded.

        Returns:
            list: The embedding vector for the input text.
        """
        text_tokens = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_embedding = self.model.encode_text(text_tokens)
        return text_embedding.cpu().numpy().tolist()[0]

    def generate_image_embedding(self, image: Image.Image) -> list:
        """
        Generates an image embedding for a given PIL Image.

        Args:
            image (Image.Image): The input image to be embedded.

        Returns:
            list: The embedding vector for the input image.
        """
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_embedding = self.model.encode_image(image)
        return image_embedding.cpu().numpy().tolist()[0]

clip_model_wrapper = CLIPModelWrapper()

async def fetch_image(session: aiohttp.ClientSession, url: str) -> Image.Image:
    """
    Fetches an image from a given URL using an aiohttp session.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for fetching the image.
        url (str): The URL of the image to fetch.

    Returns:
        Image.Image: The fetched PIL Image if successful, None otherwise.
    """
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            return Image.open(io.BytesIO(image_data))
        return None
