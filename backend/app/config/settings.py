"""Centralized application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "HR Knowledge Hub"
    app_version: str = "0.1.0"
    environment: str = "development"
    log_level: str = "INFO"

    backend_url: str = "http://localhost:8000"
    cors_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
