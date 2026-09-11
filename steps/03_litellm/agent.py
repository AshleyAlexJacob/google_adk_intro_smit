"""Step 3 — Model flexibility via LiteLLM.

Matches campus_assistant.py — v3 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
Only the model= line changes; tools and instructions stay the same.
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


def check_class_schedule(day: str) -> dict:
    """Look up SMIT Peshawar classes for a given weekday.

    Args:
        day: Weekday name such as Monday or Tuesday.

    Returns:
        A dict with status and the class title/time.
    """
    classes = {
        "Monday": "Python Basics, 6 PM",
        "Tuesday": "Agentic AI with Google ADK, 6 PM",
        "Wednesday": "Prompt Engineering, 6 PM",
        "Thursday": "Multi-Agent Systems, 6 PM",
        "Friday": "Project Lab, 6 PM",
        "Saturday": "Weekend Workshop, 10 AM",
    }
    return {"status": "success", "class": classes.get(day, "None")}


def pick_model():
    """Swap Gemini / OpenAI / Anthropic without rewriting the agent."""
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "openai":
        # Same agent, a different LLM provider
        return LiteLlm(model=os.getenv("LITELLM_MODEL", "openai/gpt-4o-mini"))
    if provider == "anthropic":
        return LiteLlm(
            model=os.getenv("LITELLM_MODEL", "anthropic/claude-3-5-sonnet-20241022")
        )
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


root_agent = LlmAgent(
    name="campus_assistant",
    model=pick_model(),
    description="SMIT campus assistant with a swappable LiteLLM model slot.",
    instruction=(
        "You are a friendly SMIT Peshawar campus assistant. "
        "Use check_class_schedule when a student asks what class is on a given day."
    ),
    tools=[check_class_schedule],
)
