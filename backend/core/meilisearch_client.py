import meilisearch
from core.config import settings

# Initialize Meilisearch client
client = meilisearch.Client(f'http://{settings.meilisearch_host}:{settings.meilisearch_port}')

# Ensure the products index exists
def create_index():
    client.create_index(uid='products', options={'primaryKey': 'id'})

create_index()
