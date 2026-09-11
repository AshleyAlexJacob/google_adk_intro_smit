"""Step 8 — Agent-to-agent delegation.

Matches campus_assistant.py — v8 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
Delegation hands off the whole turn. ADK's transfer tool carries conversation state.
"""

from pathlib import Path

from google.adk.agents import LlmAgent


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


def read_campus_doc(filename: str) -> dict:
    """Read a campus document by file name, for example timetable.md."""
    path = _docs_dir() / Path(filename).name
    if not path.is_file():
        available = [p.name for p in _docs_dir().glob("*") if p.is_file()]
        return {
            "status": "error",
            "message": f"Unknown document '{filename}'. Available: {available}",
        }
    return {"status": "success", "filename": path.name, "content": path.read_text(encoding="utf-8")}


schedule_agent = LlmAgent(
    name="schedule_agent",
    model="gemini-2.0-flash",
    description="Handles SMIT class timetable and weekly schedule questions.",
    instruction="""
You answer timetable questions for SMIT Peshawar.
Always call check_class_schedule for a specific weekday.

If the question is about course content, campus facilities, or documents
rather than the weekly timetable, call transfer_to_agent with
agent_name "docs_agent". ADK performs the handoff and carries the
conversation state — no manual state passing.
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

If the question is only about what class meets on a weekday,
call transfer_to_agent with agent_name "schedule_agent".
""",
    tools=[read_campus_doc],
)

root_agent = LlmAgent(
    name="campus_router",
    model="gemini-2.0-flash",
    description="Routes and delegates SMIT student questions between specialists.",
    instruction=(
        "Route schedule vs docs questions. "
        "Delegate timetable questions to schedule_agent and document questions "
        "to docs_agent. Specialists may transfer_to_agent if the topic changes."
    ),
    sub_agents=[schedule_agent, docs_agent],
)
