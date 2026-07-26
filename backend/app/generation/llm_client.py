"""NVIDIA NIM LLM client — one responsibility: call the model, return the answer text."""

import requests

from app.config.settings import get_settings


class LLMError(Exception):
    """Raised when the LLM API call fails."""


class NVIDIALLMClient:
    """Thin wrapper around the NVIDIA NIM chat completions endpoint."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def generate(self, prompt: str) -> str:
        """Send the prompt to the LLM and return the generated answer text."""
        try:
            response = requests.post(
                self._settings.nvidia_llm_url,
                headers={"Authorization": f"Bearer {self._settings.nvidia_llm_api_key}"},
                json={
                    "model": self._settings.nvidia_llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
                timeout=60,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMError(f"NVIDIA LLM request failed: {exc}") from exc

        return response.json()["choices"][0]["message"]["content"]


# Shared instance so generation reuses one client instead of creating a new
# one on every chat request.
llm_client = NVIDIALLMClient()
