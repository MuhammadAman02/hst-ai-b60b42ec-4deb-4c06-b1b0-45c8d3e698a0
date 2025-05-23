from pydantic_settings import BaseSettings
import os
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "My Enterprise App"
    APP_VERSION: str = "1.0.0"  # Semantic versioning
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields in environment variables

settings = Settings()