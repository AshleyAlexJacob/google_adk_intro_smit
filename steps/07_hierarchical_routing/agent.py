from pathlib import Path

from google.adk.agents import LlmAgent

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

def read_campus_doc(filename: str) -> dict:
    """Read a campus file such as timetable.md or campus_guide.md."""
    path = Path("docs") / filename
    if not path.exists():
        return {"status": "error", "message": f"File not found: {filename}"}
    return {"status": "success", "content": path.read_text()}


schedule_agent = LlmAgent(
    name="schedule_agent",
    model="gemini-2.0-flash",
    description="Answers timetable questions.",
    tools=[check_class_schedule],
)

docs_agent = LlmAgent(
    name="docs_agent",
    model="gemini-2.0-flash",
    description="Answers questions from campus documents.",
    tools=[read_campus_doc],
)

# Root agent reads the question and routes it to a focused sub-agent
root_agent = LlmAgent(
    name="campus_router",
    model="gemini-2.0-flash",
    instruction="Route schedule vs docs questions.",
    sub_agents=[schedule_agent, docs_agent],
)
\n