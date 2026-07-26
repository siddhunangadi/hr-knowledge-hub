"""Generates text embeddings via the NVIDIA NIM embedding API."""

import requests

from app.config.settings import get_settings


class EmbeddingError(Exception):
    """Raised when the embedding API call fails."""


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Call the NVIDIA NIM embedding API and return one vector per text."""
    settings = get_settings()

    try:
        response = requests.post(
            settings.nvidia_embedding_url,
            headers={"Authorization": f"Bearer {settings.nvidia_api_key}"},
            json={
                "input": texts,
                "model": settings.nvidia_embedding_model,
                "input_type": "passage",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise EmbeddingError(f"NVIDIA embedding request failed: {exc}") from exc

    data = response.json()["data"]
    return [item["embedding"] for item in data]
