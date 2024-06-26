from core.meilisearch_client import meili_client


class MeiliSearchService:
    """
    Service class for interacting with the MeiliSearch client.

    This class provides methods to search for products in the MeiliSearch index.
    """

    def __init__(self):
        """Initializes the MeiliSearchService with the 'products' index."""
        self.index = meili_client.index('products')

    async def search_products(self, query: str, limit: int = 20, offset: int = 0, filter: list = [], sort: list = []):
        """
        Searches for products in the MeiliSearch index based on the provided query parameters.

        Args:
            query (str): The search query string.
            limit (int, optional): The maximum number of results to return. Defaults to 20.
            offset (int, optional): The number of results to skip before starting to collect the result set. Defaults to 0.
            filter (list, optional): A list of filters to apply to the search results. Defaults to an empty list.
            sort (list, optional): A list of sorting criteria. Defaults to an empty list.

        Returns:
            dict: The search results returned by MeiliSearch.
        """
        search_params = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'sort': sort
        }
        return self.index.search(query, search_params)

    def search_products_by_ids(self, product_ids: list):
        results = []
        for product_id in product_ids:
            result = self.index.get_document(product_id)
            if result:
                results.append(dict(result))
        return results

    async def search_products_by_keywords(self, keywords: list, limit: int = 20, offset: int = 0):
        # Construct the query by joining keywords with space
        query = " ".join(keywords)
        
        search_params = {
            'filter': ['name IS NOT NULL', 'description IS NOT NULL', 'category_name IS NOT NULL', 'brand_name IS NOT NULL'],
            'limit': limit,
            'offset': offset,
        }

        return self.index.search(query, search_params)
