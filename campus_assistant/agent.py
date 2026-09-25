from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")

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
    model=MODEL,
    description="Answers timetable questions.",
    tools=[check_class_schedule],
)

docs_agent = LlmAgent(
    name="docs_agent",
    model=MODEL,
    description="Answers questions from campus documents.",
    tools=[read_campus_doc],
)

# Root agent reads the question and routes it to a focused sub-agent
root_agent = LlmAgent(
    name="campus_router",
    model=MODEL,
    instruction="""
    You are a senior Campus Assistant that answers questions using the appropriate sub-agent and available campus information.
For route/schedule questions, use the Route/Schedule Agent; for documentation/academic information, use the Docs Agent.
Only answer questions relevant to the campus assistant’s supported scope; politely decline unrelated requests and redirect users to campus-related topics.
Do not rely on assumptions or general knowledge when a relevant sub-agent is available; use only verified information returned by the delegated agent.
If multiple domains are involved, delegate to all relevant sub-agents and synthesize their responses without inventing details.
If the required information is unavailable, clearly state that it is unavailable rather than hallucinating.
    """,
    sub_agents=[schedule_agent, docs_agent],
)
