import json
import asyncio
from utils import clip_model_wrapper, fetch_image
from repositories.image_repository import ImageRepository
from qdrant_client.http.models import PointStruct
import aiohttp

async def process_images(json_file: str, batch_size: int = 100):
    """
    Processes images from a JSON file in batches, generates embeddings using CLIP,
    and uploads them to Qdrant.

    Args:
        json_file (str): The path to the JSON file containing product information.
        batch_size (int, optional): The number of products to process in each batch. Defaults to 100.
    """
    image_repository = ImageRepository()

    async with aiohttp.ClientSession() as session:
        with open(json_file, "r") as f:
            products = json.load(f)

        tasks = []
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]
            for product in batch:
                product_id = product["id"]
                for image_url in product["images"]:
                    tasks.append(process_image(product_id, image_url, session, image_repository))

            await asyncio.gather(*tasks)
            tasks = []  # Clear tasks after processing each batch

async def process_image(product_id: int, image_url: str, session: aiohttp.ClientSession, image_repository: ImageRepository):
    """
    Processes a single image: fetches the image, generates its embedding, and uploads it to Qdrant.

    Args:
        product_id (int): The ID of the product.
        image_url (str): The URL of the image to process.
        session (aiohttp.ClientSession): The aiohttp session to use for fetching the image.
        image_repository (ImageRepository): The repository for uploading image embeddings.
    """
    image = await fetch_image(session, image_url)
    if image:
        embedding = clip_model_wrapper.generate_image_embedding(image)
        point = PointStruct(id=f"{product_id}_{image_url}", vector=embedding, payload={"product_id": product_id, "url": image_url})
        await image_repository.upsert_images([point])

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1]
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100  # Default batch size is 100
    asyncio.run(process_images(json_file, batch_size))
