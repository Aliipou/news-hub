"""
Configuration management for the News Aggregator backend.
Handles environment variables and application settings.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # NewsAPI Configuration
    news_api_key: str = "test_api_key"  # Default for testing, override in .env
    news_api_base_url: str = "https://newsapi.org/v2"

    # Application Configuration
    app_name: str = "News Aggregator API"
    app_version: str = "1.0.0"
    debug: bool = False

    # CORS Configuration
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

    # Cache Configuration (in seconds)
    cache_ttl: int = 180  # 3 minutes

    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()
