"""NVIDIA NIM embedding client — one responsibility: generate embeddings."""

import requests

from app.config.settings import get_settings


class EmbeddingError(Exception):
    """Raised when the embedding API call fails."""


class NVIDIAEmbeddingClient:
    """Thin wrapper around the NVIDIA NIM embedding endpoint."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def embed(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        """Return one embedding vector per input text.

        input_type is "passage" for document chunks and "query" for search
        queries — the embedding model treats them asymmetrically.
        """
        try:
            response = requests.post(
                self._settings.nvidia_embedding_url,
                headers={"Authorization": f"Bearer {self._settings.nvidia_api_key}"},
                json={
                    "input": texts,
                    "model": self._settings.nvidia_embedding_model,
                    "input_type": input_type,
                },
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise EmbeddingError(f"NVIDIA embedding request failed: {exc}") from exc

        data = response.json()["data"]
        return [item["embedding"] for item in data]
