from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    
    # Application Settings
    APP_NAME: str = "MINDSHEAR.AI"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SITE_URL: str = os.getenv("SITE_URL", "http://localhost:8000")
    SITE_NAME: str = "MINDSHEAR.AI"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    TEMP_DIR: str = "temp"
    VECTOR_STORE_DIR: str = "vector_store"
    
    # AI Model Settings
    GEMINI_MODEL: str = "gemini-pro"
    CLIP_MODEL: str = "openai/clip-vit-base-patch32"
    DEEPSEEK_MODEL: str = "deepseek/deepseek-r1:free"
    
    # Image Settings
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/gif"]
    
    class Config:
        case_sensitive = True

settings = Settings()

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True) 