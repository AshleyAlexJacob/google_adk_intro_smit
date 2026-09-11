"""Step 6 — Bidirectional audio and video streaming.

Matches campus_assistant.py — v6 in SMIT_Peshawar_ADK_Agentic_AI.pdf.

True live audio/video uses runner.run_live() with a LiveRequestQueue.
This step keeps the same agent and tools, then exposes two run modes:

- Text CLI streaming: RunConfig(streaming_mode=StreamingMode.SSE)
- Live / kiosk style: RunConfig(streaming_mode=StreamingMode.BIDI) + run_live()
"""

from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig, StreamingMode


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
    description="Campus assistant that can stream replies for a live campus kiosk.",
    instruction=(
        "You are a friendly SMIT Peshawar campus assistant. "
        "Keep spoken-style answers short. Use check_class_schedule for timetable questions."
    ),
    tools=[check_class_schedule],
)

# Live / bidirectional mode (audio-video kiosk). chat.py uses SSE for the text CLI.
run_config = RunConfig(streaming_mode=StreamingMode.BIDI)
sse_run_config = RunConfig(streaming_mode=StreamingMode.SSE)
