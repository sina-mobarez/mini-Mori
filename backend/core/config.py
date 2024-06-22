from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A Pydantic BaseSettings class for configuration settings.

    Attributes:
        qdrant_host (str): The host address of the Qdrant service. Default is "localhost".
        qdrant_port (int): The port number of the Qdrant service. Default is 6333.
    """
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    class Config:
        """
        Configuration class for Settings.

        Attributes:
            env_file (str): The path to the environment file to load settings from.
        """
        env_file = ".env"

# Instantiate the settings
settings = Settings()

