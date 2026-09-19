from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm


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





# MCP: one protocol to connect an external tool server (here: local docs folder)
docs_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "./docs"],
        )
    )
)

root_agent = LlmAgent(
    name="campus_assistant",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="Use schedule and docs tools to help students.",
    tools=[check_class_schedule, read_campus_doc, docs_tools],
)
