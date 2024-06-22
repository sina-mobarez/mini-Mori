import torch
import clip
from PIL import Image
import io

class CLIPModelWrapper:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def generate_text_embedding(self, text: str):
        text_tokens = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_embedding = self.model.encode_text(text_tokens)
        return text_embedding.cpu().numpy().tolist()[0]

    def generate_image_embedding(self, image: Image.Image):
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_embedding = self.model.encode_image(image)
        return image_embedding.cpu().numpy().tolist()[0]

clip_model_wrapper = CLIPModelWrapper()


async def fetch_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            return Image.open(io.BytesIO(image_data))
        return None