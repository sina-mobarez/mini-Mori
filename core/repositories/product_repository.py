from db.postgres_client import postgres_client

class ProductRepository:
    def __init__(self):
        self.client = postgres_client
    
    async def search_products(self, query: str, limit: int = 20, offset: int = 0, filter: list = [], sort: list = []):
        """
        Searches for products in the PostgreSQL database based on the provided query parameters.
        
        Args:
            query (str): The search query string.
            limit (int): The maximum number of results to return.
            offset (int): The number of results to skip.
            filter (list): A list of filters to apply to the search results.
            sort (list): A list of sorting criteria.
            
        Returns:
            dict: The search results.
        """
        conn = self.client.get_connection()
        try:
            with conn.cursor() as cur:
                # Build the WHERE clause based on filters
                where_clauses = ["search_vector @@ plainto_tsquery('english', %s)"]
                params = [query]
                
                for f in filter:
                    if ":" in f:
                        field, value = f.split(":", 1)
                        where_clauses.append(f"{field} = %s")
                        params.append(value)
                
                # Build the ORDER BY clause based on sort
                order_clause = ""
                if sort:
                    order_parts = []
                    for s in sort:
                        if s.startswith("-"):
                            order_parts.append(f"{s[1:]} DESC")
                        else:
                            order_parts.append(f"{s} ASC")
                    order_clause = f"ORDER BY {', '.join(order_parts)}"
                else:
                    order_clause = "ORDER BY ts_rank(search_vector, plainto_tsquery('english', %s)) DESC"
                    params.append(query)
                
                # Build the complete query
                sql = f"""
                SELECT *
                FROM products
                WHERE {' AND '.join(where_clauses)}
                {order_clause}
                LIMIT %s OFFSET %s
                """
                params.extend([limit, offset])
                
                cur.execute(sql, params)
                columns = [desc[0] for desc in cur.description]
                results = []
                for row in cur.fetchall():
                    result = dict(zip(columns, row))
                    results.append(result)
                
                return {
                    "hits": results,
                    "limit": limit,
                    "offset": offset
                }
        finally:
            self.client.release_connection(conn)
    
    def search_products_by_ids(self, product_ids: list):
        """
        Searches for products based on a list of IDs.
        
        Args:
            product_ids (list): List of product IDs.
            
        Returns:
            list: A list of products matching the provided IDs.
        """
        conn = self.client.get_connection()
        try:
            with conn.cursor() as cur:
                placeholders = ", ".join(["%s"] * len(product_ids))
                cur.execute(
                    f"SELECT * FROM products WHERE id IN ({placeholders})",
                    product_ids
                )
                columns = [desc[0] for desc in cur.description]
                results = []
                for row in cur.fetchall():
                    result = dict(zip(columns, row))
                    results.append(result)
                return results
        finally:
            self.client.release_connection(conn)
    
    async def search_products_by_keywords(self, keywords: list, limit: int = 20, offset: int = 0):
        """
        Searches for products based on a list of keywords.
        
        Args:
            keywords (list): List of keywords.
            limit (int): The maximum number of results to return.
            offset (int): The number of results to skip.
            
        Returns:
            dict: The search results.
        """
        query = " & ".join(keywords)
        conn = self.client.get_connection()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT *
                FROM products
                WHERE search_vector @@ to_tsquery('english', %s)
                ORDER BY ts_rank(search_vector, to_tsquery('english', %s)) DESC
                LIMIT %s OFFSET %s
                """
                cur.execute(sql, (query, query, limit, offset))
                columns = [desc[0] for desc in cur.description]
                results = []
                for row in cur.fetchall():
                    result = dict(zip(columns, row))
                    results.append(result)
                
                return {
                    "hits": results,
                    "limit": limit,
                    "offset": offset
                }
        finally:
            self.client.release_connection(conn)