"""Pitch Master — LLM Provider Implementations."""

from __future__ import annotations

import traceback


def call_openai(prompt: str, system_prompt: str | None, model: str, temperature: float) -> str:
    """Call OpenAI API."""
    from openai import OpenAI
    from pitch_master.config import OPENAI_API_KEY

    if not OPENAI_API_KEY:
        raise ValueError("Missing API key for provider: openai. Please set it in .env")

    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def call_anthropic(prompt: str, system_prompt: str | None, model: str, temperature: float) -> str:
    """Call Anthropic Claude API."""
    from anthropic import Anthropic
    from pitch_master.config import ANTHROPIC_API_KEY

    if not ANTHROPIC_API_KEY:
        raise ValueError("Missing API key for provider: anthropic. Please set it in .env")

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    kwargs = {
        "model": model,
        "max_tokens": 4096,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    response = client.messages.create(**kwargs)
    return response.content[0].text


def call_google(prompt: str, system_prompt: str | None, model: str, temperature: float) -> str:
    """Call Google Gemini API."""
    from google import genai
    from pitch_master.config import GOOGLE_API_KEY

    if not GOOGLE_API_KEY:
        raise ValueError("Missing API key for provider: google. Please set it in .env")

    client = genai.Client(api_key=GOOGLE_API_KEY)
    contents = []
    if system_prompt:
        contents.append({"role": "user", "parts": [{"text": system_prompt}]})
        contents.append({"role": "model", "parts": [{"text": "Understood."}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config={"temperature": temperature},
    )
    return response.text or ""


def call_groq(prompt: str, system_prompt: str | None, model: str, temperature: float) -> str:
    """Call Groq API."""
    from groq import Groq
    from pitch_master.config import GROQ_API_KEY

    if not GROQ_API_KEY:
        raise ValueError("Missing API key for provider: groq. Please set it in .env")

    client = Groq(api_key=GROQ_API_KEY)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def call_openrouter(prompt: str, system_prompt: str | None, model: str, temperature: float) -> str:
    """Call OpenRouter API (uses OpenAI-compatible interface)."""
    from openai import OpenAI
    from pitch_master.config import OPENROUTER_API_KEY

    if not OPENROUTER_API_KEY:
        raise ValueError("Missing API key for provider: openrouter. Please set it in .env")

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
