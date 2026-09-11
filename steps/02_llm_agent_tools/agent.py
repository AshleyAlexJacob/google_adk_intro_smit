"""Step 2 — LlmAgent, tools, and orchestration.

Matches campus_assistant.py — v2 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
A tool is a normal Python function. ADK decides when to call it.
"""

from google.adk.agents import LlmAgent


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


root_agent = LlmAgent(
    name="campus_assistant",
    model="gemini-2.0-flash",
    description="SMIT campus assistant that can check the weekly class schedule.",
    instruction=(
        "You are a friendly SMIT Peshawar campus assistant. "
        "Use check_class_schedule when a student asks what class is on a given day. "
        "Accept common day names such as Mon or Monday."
    ),
    tools=[check_class_schedule],
)
