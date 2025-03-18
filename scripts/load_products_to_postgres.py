import json
from pathlib import Path
import sys
import psycopg2 as psycopg

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from core.config import settings

def load_products(json_file: str):
    """
    Load products from a JSON file and add them to the PostgreSQL database.
    
    Args:
        json_file (str): The path to the JSON file containing the product data.
    """
    with open(json_file, 'r') as f:
        products = json.load(f)
    
    connection_string = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            for product in products:
                # Convert arrays to PostgreSQL arrays
                images = product.get("images", [])
                colors = product.get("colors", [])
                sizes = product.get("sizes", [])
                
                cur.execute(
                    """
                    INSERT INTO products (
                        id, name, description, material, rating, images, code,
                        brand_id, brand_name, category_id, category_name,
                        gender_id, gender_name, shop_id, shop_name,
                        link, status, colors, sizes, region, currency,
                        current_price, old_price, off_percent, update_date
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    ) ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        material = EXCLUDED.material,
                        rating = EXCLUDED.rating,
                        images = EXCLUDED.images,
                        code = EXCLUDED.code,
                        brand_id = EXCLUDED.brand_id,
                        brand_name = EXCLUDED.brand_name,
                        category_id = EXCLUDED.category_id,
                        category_name = EXCLUDED.category_name,
                        gender_id = EXCLUDED.gender_id,
                        gender_name = EXCLUDED.gender_name,
                        shop_id = EXCLUDED.shop_id,
                        shop_name = EXCLUDED.shop_name,
                        link = EXCLUDED.link,
                        status = EXCLUDED.status,
                        colors = EXCLUDED.colors,
                        sizes = EXCLUDED.sizes,
                        region = EXCLUDED.region,
                        currency = EXCLUDED.currency,
                        current_price = EXCLUDED.current_price,
                        old_price = EXCLUDED.old_price,
                        off_percent = EXCLUDED.off_percent,
                        update_date = EXCLUDED.update_date
                    """,
                    (
                        product.get("id"), product.get("name"), product.get("description"),
                        product.get("material"), product.get("rating"), images, product.get("code"),
                        product.get("brand_id"), product.get("brand_name"),
                        product.get("category_id"), product.get("category_name"),
                        product.get("gender_id"), product.get("gender_name"),
                        product.get("shop_id"), product.get("shop_name"),
                        product.get("link"), product.get("status"),
                        colors, sizes,
                        product.get("region"), product.get("currency"),
                        product.get("current_price"), product.get("old_price"),
                        product.get("off_percent"), product.get("update_date")
                    )
                )
            
            conn.commit()
            print(f"Successfully loaded {len(products)} products into the database")

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1]
    load_products(json_file)