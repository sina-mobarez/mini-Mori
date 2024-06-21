from pydantic import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str
    qdrant_port: int 

    class Config:
        env_file = ".env"

settings = Settings()
