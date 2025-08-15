from pydantic_settings import BaseSettings
import os
from dotenv import dotenv_values

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""

    # Dynamically add all .env variables as attributes
    def __init__(self, **kwargs):
        # Look for .env in backend directory
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        env_path = os.path.join(backend_dir, ".env")
        env_vars = dotenv_values(env_path)
        kwargs.update(env_vars)
        super().__init__(**kwargs)

settings = Settings()
