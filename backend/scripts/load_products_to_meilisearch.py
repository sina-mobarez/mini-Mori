import json
from core.meilisearch_client import meili_client

def load_products(json_file: str):
    """
    Load products from a JSON file and add them to the MeiliSearch index.

    Args:
        json_file (str): The path to the JSON file containing the product data.
    """
    with open(json_file, 'r') as f:
        products = json.load(f)

    index = meili_client.index('products')
    index.add_documents(products)

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1]
    load_products(json_file)

