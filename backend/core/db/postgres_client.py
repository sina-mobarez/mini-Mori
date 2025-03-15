from psycopg_pool import ConnectionPool
from core.config import settings

class PostgresClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
            connection_string = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
            cls._instance.pool = ConnectionPool(connection_string, min_size=5, max_size=20)
        return cls._instance
    
    def get_connection(self):
        return self.pool.getconn()
    
    def release_connection(self, conn):
        self.pool.putconn(conn)

postgres_client = PostgresClient()