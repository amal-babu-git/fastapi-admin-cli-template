"""
Application configuration.
"""
import os
from typing import Optional, Dict, Any, List

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings."""
    
    PROJECT_NAME: str = "{{ project_name }}"
    API_V1_STR: str = "/api/v1"
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./app.db"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
