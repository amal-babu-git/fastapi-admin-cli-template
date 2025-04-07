from pydantic_settings import BaseSettings
from typing import Optional, List
import logging

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "API Title"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "API Description"
    API_PORT: int = 8000
    API_DOMAIN: str = "api.example.com"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "app_db"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "postgres"
    DATABASE_URL: Optional[str] = None

    # Traefik Settings
    TRAEFIK_DASHBOARD_HOST: str = "traefik.example.com"
    TRAEFIK_DASHBOARD_AUTH: str = "admin:password"
    ACME_EMAIL: str = "admin@example.com"

    # Environment Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Auth Settings
    SECRET_KEY: str = "secret-key-change-in-production"
    JWT_SECRET: str = "jwt-secret-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Settings
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_FROM_NAME: str = "App Name"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    @property
    def get_database_url(self) -> str:
        """Get the database URL, either from DATABASE_URL or construct from components."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    def configure_logging(self) -> None:
        """Configure logging based on environment settings."""
        log_level = getattr(logging, self.LOG_LEVEL)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
        
        # Set lower log levels for noisy libraries in production
        if not self.DEBUG:
            logging.getLogger("uvicorn").setLevel(logging.WARNING)
            logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create the settings instance
settings = Settings()
