"""Pitch Master — LLM Router.

Routes requests to the configured provider.
Single entry point: generate_text(prompt, system_prompt) -> str
"""

from __future__ import annotations

import traceback

from pitch_master.config import LLM_PROVIDER, LLM_MODEL, TEMPERATURE
from pitch_master.providers import (
    call_openai,
    call_anthropic,
    call_google,
    call_groq,
    call_openrouter,
)

PROVIDERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "google": call_google,
    "groq": call_groq,
    "openrouter": call_openrouter,
}


def generate_text(prompt: str, system_prompt: str | None = None) -> str:
    """Generate text using the configured LLM provider.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.

    Returns:
        Generated text from the LLM.

    Raises:
        ValueError: If provider is unknown or API key is missing.
    """
    provider = LLM_PROVIDER.lower().strip()

    if provider not in PROVIDERS:
        available = ", ".join(PROVIDERS.keys())
        raise ValueError(
            f"Unknown LLM provider: '{provider}'. "
            f"Available providers: {available}. "
            f"Set LLM_PROVIDER in .env"
        )

    try:
        return PROVIDERS[provider](prompt, system_prompt, LLM_MODEL, TEMPERATURE)
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(
            f"LLM call failed (provider={provider}, model={LLM_MODEL}): {e}\n"
            f"{traceback.format_exc()}"
        )
