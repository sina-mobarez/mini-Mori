from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A Pydantic BaseSettings class for configuration settings.

    Attributes:
        qdrant_host (str): The host address of the Qdrant service. Default is "localhost".
        qdrant_port (int): The port number of the Qdrant service. Default is 6333.
        meilisearch_host (str): The host for MeiliSearch.
        meilisearch_port (int): The port for MeiliSearch.
    """
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    meilisearch_host: str = "localhost"
    meilisearch_port: int = 7700

    class Config:
        """
        Configuration class for Settings.

        Attributes:
            env_file (str): The path to the environment file to load settings from.
        """
        env_file = ".env"

# Instantiate the settings
settings = Settings()

