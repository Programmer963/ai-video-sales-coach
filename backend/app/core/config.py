from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Video Sales Coach"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_VIDEO_EXTENSIONS: List[str] = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    
    # AI Service Settings
    ENABLE_EMOTION_DETECTION: bool = True
    ENABLE_SPEECH_ANALYSIS: bool = True
    ENABLE_TEXT_ANALYSIS: bool = True
    
    # External API Keys (set via environment variables)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/sales_coach_db"
    
    # Redis Settings
    REDIS_URL: str = "redis://redis:6379"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 