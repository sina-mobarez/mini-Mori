import json
from core.meilisearch_client import client

def load_products(json_file):
    with open(json_file, 'r') as f:
        products = json.load(f)

    index = client.index('products')
    index.add_documents(products)

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1]
    load_products(json_file)
