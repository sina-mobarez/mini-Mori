import meilisearch
from core.config import settings


class MeiliSearchClient:
    """
    MeiliSearch client wrapper for initializing and ensuring the products index exists.

    Attributes:
        client (meilisearch.Client): The MeiliSearch client instance.
    """

    def __init__(self):
        self.client = meilisearch.Client(
            f'http://{settings.meilisearch_host}:{settings.meilisearch_port}')
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        """
        Ensure the 'products' index exists in MeiliSearch.
        If the index does not exist, it creates one with 'id' as the primary key.
        """
        if 'products' not in [index for index in self.client.get_indexes()]:
            self.client.create_index(uid='products', options={
                'primaryKey': 'id',
            })

        self.client.index('products').update_filterable_attributes([
            'name',
            'description',
            'brand_name',
            'category_name'
        ])


# Initialize the MeiliSearch client
meili_client = MeiliSearchClient().client
