"""
Configuration management.

Loads and validates environment variables using pydantic-settings.
"""
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database configuration
    # Required: Set DATABASE_URL in .env file or environment variable
    # Format: postgresql+asyncpg://user:password@host:port/dbname
    # See .env.example for local development example
    database_url: str  # Required - no default to prevent hardcoded credentials
    
    # OpenAI API configuration
    openai_api_key: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables not defined in Settings
    )


settings = Settings()

# Log warning if OpenAI API key is not set (but don't fail)
if not settings.openai_api_key:
    logger.warning(
        "OPENAI_API_KEY is not set. "
        "OpenAI API features will not be available. "
        "Set OPENAI_API_KEY in .env file to enable OpenAI integration."
    )

