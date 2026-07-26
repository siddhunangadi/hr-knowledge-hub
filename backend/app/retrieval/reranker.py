"""NVIDIA NIM reranker client — one responsibility: rerank candidate passages."""

import requests

from app.config.settings import get_settings


class RerankError(Exception):
    """Raised when the reranker API call fails."""


class NVIDIARerankerClient:
    """Thin wrapper around the NVIDIA NIM reranking endpoint."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def rerank(self, query: str, passages: list[str]) -> list[dict]:
        """Return {index, score} for each passage, sorted most relevant first.

        `index` refers to the passage's position in the input list.
        """
        try:
            response = requests.post(
                self._settings.nvidia_reranker_url,
                headers={"Authorization": f"Bearer {self._settings.nvidia_api_key}"},
                json={
                    "model": self._settings.nvidia_reranker_model,
                    "query": {"text": query},
                    "passages": [{"text": passage} for passage in passages],
                },
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RerankError(f"NVIDIA reranker request failed: {exc}") from exc

        rankings = response.json()["rankings"]
        return [{"index": item["index"], "score": item["logit"]} for item in rankings]
