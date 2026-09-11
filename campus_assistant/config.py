"""Shared paths and model selection for the SMIT campus assistant."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DOCS_DIR = ROOT / "docs"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "openai/gpt-4o-mini")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()


def pick_model():
    """LiteLLM-ready model slot: swap providers without rewriting agents."""
    if LLM_PROVIDER == "openai":
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=LITELLM_MODEL)
    if LLM_PROVIDER == "anthropic":
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=os.getenv("LITELLM_MODEL", "anthropic/claude-3-5-sonnet-20241022"))
    return GEMINI_MODEL
