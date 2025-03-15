from core.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    async def search_products(self, query: str, limit: int = 20, offset: int = 0, filter: list = [], sort: list = []):
        return await self.repository.search_products(query, limit, offset, filter, sort)
    
    def search_products_by_ids(self, product_ids: list):
        return self.repository.search_products_by_ids(product_ids)
    
    async def search_products_by_keywords(self, keywords: list, limit: int = 20, offset: int = 0):
        return await self.repository.search_products_by_keywords(keywords, limit, offset)