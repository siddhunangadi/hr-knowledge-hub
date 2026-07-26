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
    cors_origins: list[str] = ["*"]

    # NVIDIA NIM embedding API
    nvidia_embedding_api_key: str = ""
    nvidia_embedding_url: str = "https://integrate.api.nvidia.com/v1/embeddings"
    nvidia_embedding_model: str = "nvidia/nv-embedqa-e5-v5"

    # NVIDIA NIM reranker API
    nvidia_reranker_api_key: str = ""
    nvidia_reranker_url: str = (
        "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-nemotron-rerank-vl-1b-v2/reranking"
    )
    nvidia_reranker_model: str = "nvidia/llama-nemotron-rerank-vl-1b-v2"

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index_name: str = "hr-knowledge-hub"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
