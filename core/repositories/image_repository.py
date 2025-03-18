from db.postgres_client import postgres_client
import numpy

class ImageRepository:
    def __init__(self):
        self.client = postgres_client
    
    async def upsert_images(self, points: list):
        """
        Upserts (inserts or updates) image embeddings into the PostgreSQL database.
        
        Args:
            points (list): A list of points with id, product_id, url, and embedding.
        """
        conn = self.client.get_connection()
        try:
            with conn.cursor() as cur:
                for point in points:
                    cur.execute(
                        """
                        INSERT INTO image_embeddings (id, product_id, url, embedding)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE
                        SET embedding = EXCLUDED.embedding
                        """,
                        (point.id, point.payload["product_id"], point.payload["url"], point.vector)
                    )
            conn.commit()
        finally:
            self.client.release_connection(conn)
    
    async def search_similar_images(self, embedding: list, limit: int = 5) -> list:
        """
        Searches for images similar to the given embedding using cosine similarity.
        
        Args:
            embedding (list): The embedding vector to search for similar images.
            limit (int, optional): The maximum number of similar images to return.
            
        Returns:
            list: A list of search results containing similar images with their details.
        """
        conn = self.client.get_connection()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 
                        id, 
                        product_id, 
                        url, 
                        1 - (embedding <-> %s) / 2 as similarity
                    FROM image_embeddings
                    ORDER BY similarity DESC
                    LIMIT %s
                    """,
                    (str(embedding), limit)
                )
                results = []
                for row in cur.fetchall():
                    results.append({
                        "id": row[0],
                        "product_id": row[1],
                        "url": row[2],
                        "score": float(row[3])
                    })
                return results
        finally:
            self.client.release_connection(conn)