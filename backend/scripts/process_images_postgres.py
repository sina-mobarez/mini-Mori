import json
from pathlib import Path
import sys
import asyncio
import aiohttp
import psycopg2 as psycopg

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from core.utils import clip_model_wrapper, fetch_image
from core.config import settings

async def process_images(json_file: str, batch_size: int = 100):
    """
    Processes images from a JSON file in batches, generates embeddings using CLIP,
    and uploads them to PostgreSQL.

    Args:
        json_file (str): The path to the JSON file containing product information.
        batch_size (int, optional): The number of products to process in each batch. Defaults to 100.
    """
    connection_string = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    
    async with aiohttp.ClientSession() as session:
        with open(json_file, "r") as f:
            products = json.load(f)

        tasks = []
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]
            for product in batch:
                product_id = product["id"]
                for image_url in product["images"]:
                    tasks.append(process_image(product_id, image_url, session, connection_string))

            await asyncio.gather(*tasks)
            tasks = []  # Clear tasks after processing each batch

async def process_image(product_id: int, image_url: str, session: aiohttp.ClientSession, connection_string: str):
    """
    Processes a single image: fetches the image, generates its embedding, and uploads it to PostgreSQL.

    Args:
        product_id (int): The ID of the product.
        image_url (str): The URL of the image to process.
        session (aiohttp.ClientSession): The aiohttp session to use for fetching the image.
        connection_string (str): PostgreSQL connection string.
    """
    image = await fetch_image(session, image_url)
    if image:
        embedding = clip_model_wrapper.generate_image_embedding(image)
        
        # Create a unique ID for the image embedding
        image_id = f"{product_id}_{image_url}"
        
        # Store the embedding in PostgreSQL
        conn = await asyncio.to_thread(psycopg.connect, connection_string)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO image_embeddings (id, product_id, url, embedding)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET embedding = EXCLUDED.embedding
                    """,
                    (image_id, product_id, image_url, embedding)
                )
            conn.commit()
        finally:
            conn.close()

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1]
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100  # Default batch size is 100
    asyncio.run(process_images(json_file, batch_size))