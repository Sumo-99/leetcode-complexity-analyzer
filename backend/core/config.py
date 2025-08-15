from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")

settings = Settings()
