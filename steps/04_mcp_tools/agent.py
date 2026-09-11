"""Step 4 — Native MCP tool integration plus a custom docs tool.

Matches campus_assistant.py — v4 in SMIT_Peshawar_ADK_Agentic_AI.pdf.
"""

from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters


def _docs_dir() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parents[2] / "docs", here.parents[1] / "docs", Path.cwd() / "docs"):
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
    """Read a campus document by file name, for example timetable.md.

    Args:
        filename: Document name inside the docs folder.

    Returns:
        File contents, or an error if the file is missing.
    """
    path = _docs_dir() / Path(filename).name
    if not path.is_file():
        available = [p.name for p in _docs_dir().glob("*") if p.is_file()]
        return {
            "status": "error",
            "message": f"Unknown document '{filename}'. Available: {available}",
        }
    return {"status": "success", "filename": path.name, "content": path.read_text(encoding="utf-8")}


docs_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(_docs_dir()),
            ],
        ),
        timeout=15,
    ),
    tool_filter=["read_file", "list_directory", "search_files", "get_file_info"],
)

root_agent = LlmAgent(
    name="campus_assistant",
    model="gemini-2.0-flash",
    description="Campus assistant with a class-schedule tool and MCP filesystem access.",
    instruction=(
        "You are a friendly SMIT Peshawar campus assistant. "
        "Use check_class_schedule for timetable questions. "
        "Use read_campus_doc or the filesystem MCP tools for course docs "
        "(timetable.md, courses.md, campus_guide.md)."
    ),
    tools=[check_class_schedule, read_campus_doc, docs_tools],
)
