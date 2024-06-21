import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

class CLIPModelWrapper:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def generate_text_embedding(self, text: str) -> list:
        inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embeddings = self.model.get_text_features(**inputs).squeeze().tolist()
        return embeddings

    def generate_image_embedding(self, image: Image) -> list:
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model.get_image_features(**inputs).squeeze().tolist()
        return embeddings

clip_model_wrapper = CLIPModelWrapper()
