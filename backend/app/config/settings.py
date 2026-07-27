"""Centralized application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolved relative to this file (not the process's cwd) so `.env` at the
# project root is found whether uvicorn is launched from there or from
# backend/. Harmless if missing — e.g. in Docker, where env vars are
# injected directly instead of via a mounted .env file.
_ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

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

    # NVIDIA NIM text generation API
    nvidia_llm_api_key: str = ""
    nvidia_llm_url: str = "https://integrate.api.nvidia.com/v1/chat/completions"
    # 70B rather than 8B: the smaller model was verified to fail on indirect
    # / inferential questions (e.g. "does X from 2013 mean policy Y from
    # 2009 is still active?") even when the exact answer was the only chunk
    # in its context — it answered correctly once rephrased as a direct
    # question, so this was a reasoning-capacity issue, not a retrieval one.
    nvidia_llm_model: str = "meta/llama-3.1-70b-instruct"

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
