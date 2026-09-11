"""Step 9 — Error handling and debugging.

Matches campus_assistant.py — v9 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
Catch the error, return a clear status, and let the agent keep talking.
Debug with: python chat.py --verbose   (or: adk run --verbose)
"""

from pathlib import Path

from google.adk.agents import LlmAgent

CLASSES = {
    "Monday": "Python Basics, 6 PM",
    "Tuesday": "Agentic AI with Google ADK, 6 PM",
    "Wednesday": "Prompt Engineering, 6 PM",
    "Thursday": "Multi-Agent Systems, 6 PM",
    "Friday": "Project Lab, 6 PM",
    "Saturday": "Weekend Workshop, 10 AM",
}


def _docs_dir() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parents[2] / "docs", Path.cwd() / "docs"):
        if candidate.is_dir():
            return candidate
    return Path.cwd() / "docs"


def check_class_schedule(day: str) -> dict:
    """Look up SMIT Peshawar classes for a given weekday.

    Args:
        day: Weekday name such as Monday or Tuesday.

    Returns:
        A dict with status=success and the class, or status=error.
    """
    try:
        normalized = day.strip().title()
        aliases = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
        normalized = aliases.get(normalized, normalized)
        return {"status": "success", "class": CLASSES[normalized]}
    except KeyError:
        return {
            "status": "error",
            "message": f"No class on {day}. Valid days: {', '.join(CLASSES)}",
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {"status": "error", "message": f"Schedule lookup failed: {exc}"}


def read_campus_doc(filename: str) -> dict:
    """Read a campus document by file name, for example timetable.md."""
    try:
        path = _docs_dir() / Path(filename).name
        if not path.is_file():
            raise FileNotFoundError(filename)
        return {
            "status": "success",
            "filename": path.name,
            "content": path.read_text(encoding="utf-8"),
        }
    except FileNotFoundError:
        available = [p.name for p in _docs_dir().glob("*") if p.is_file()]
        return {
            "status": "error",
            "message": f"No document named {filename}. Available: {available}",
        }
    except OSError as exc:
        return {"status": "error", "message": f"Could not read {filename}: {exc}"}


schedule_agent = LlmAgent(
    name="schedule_agent",
    model="gemini-2.0-flash",
    description="Handles SMIT class timetable and weekly schedule questions.",
    instruction="""
You answer timetable questions for SMIT Peshawar.
Always call check_class_schedule for a specific weekday.
If the tool returns status=error, tell the student clearly and list valid days.
If the question is about course content, call transfer_to_agent with
agent_name "docs_agent".
""",
    tools=[check_class_schedule],
)

docs_agent = LlmAgent(
    name="docs_agent",
    model="gemini-2.0-flash",
    description="Answers questions from campus course documents and the campus guide.",
    instruction="""
You answer questions from SMIT course documents.
Call read_campus_doc with timetable.md, courses.md, or campus_guide.md.
If the tool returns status=error, explain what documents exist.
If the question is only about the weekday timetable, call transfer_to_agent
with agent_name "schedule_agent".
""",
    tools=[read_campus_doc],
)

root_agent = LlmAgent(
    name="campus_router",
    model="gemini-2.0-flash",
    description="Routes SMIT student questions and recovers from tool errors.",
    instruction=(
        "Route schedule vs docs questions. "
        "Never invent a class time if the schedule tool returns an error."
    ),
    sub_agents=[schedule_agent, docs_agent],
)
