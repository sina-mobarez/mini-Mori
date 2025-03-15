from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "sm"
    postgres_password: str = "admin"
    postgres_db: str = "mini_mori"
    
    class Config:
        env_file = ".env"

settings = Settings()