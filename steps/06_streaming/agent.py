from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig, StreamingMode

def check_class_schedule(day: str) -> dict:
    """Look up SMIT classes for a weekday like Monday."""
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
    instruction="Keep answers short. Use check_class_schedule for timetable questions.",
    tools=[check_class_schedule],
)

# Same agent, different run mode: SSE for text streaming, BIDI for live audio/video
run_config = RunConfig(streaming_mode=StreamingMode.SSE)
\n