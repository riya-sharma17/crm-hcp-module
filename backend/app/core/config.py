from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "CRM HCP Module"
    DEBUG: bool = True
    ALLOWED_ORIGINS: list = ["http://localhost:5173"]
    
    # Database
    DATABASE_URL: str
    
    # Groq
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()