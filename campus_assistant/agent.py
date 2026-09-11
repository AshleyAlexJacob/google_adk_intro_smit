"""Step 1 — What is ADK: an open-source, model-agnostic campus assistant.

Matches campus_assistant.py — v1 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
"""

from google.adk.agents import Agent

root_agent = Agent(
    name="campus_assistant",
    model="gemini-2.0-flash",
    description="Friendly campus assistant for SMIT Peshawar students.",
    instruction=(
        "You are a friendly SMIT Peshawar campus assistant. "
        "Help students with campus questions in a warm, concise tone. "
        "If you do not know something, say so and suggest who they can ask."
    ),
)
