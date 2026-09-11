"""Assembled SMIT Peshawar Campus Assistant — all workshop layers.

Router + schedule_agent + docs_agent, MCP docs, LiteLLM model slot,
and try/except tools. Matches campus_assistant.py — final in the PDF.
"""

from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig, StreamingMode

from campus_assistant.config import pick_model
from campus_assistant.tools import check_class_schedule, read_campus_doc, search_campus_docs

schedule_agent = LlmAgent(
    name="schedule_agent",
    model=pick_model(),
    description="Handles SMIT class timetable and weekly schedule questions.",
    instruction="""
You answer timetable questions for SMIT Peshawar.
Always call check_class_schedule for a specific weekday.
If the tool returns status=error, tell the student clearly and list valid days.
If the question is about course content, campus facilities, or documents
rather than the weekly timetable, call transfer_to_agent with
agent_name "docs_agent".
""",
    tools=[check_class_schedule],
)

docs_tools = [read_campus_doc, search_campus_docs]
if os.getenv("ENABLE_MCP", "").lower() in {"1", "true", "yes"}:
    from campus_assistant.mcp_docs import build_docs_mcp_toolset

    docs_tools.append(build_docs_mcp_toolset())

docs_agent = LlmAgent(
    name="docs_agent",
    model=pick_model(),
    description="Answers questions from campus course documents and the campus guide.",
    instruction="""
You answer questions from SMIT course documents.
Use read_campus_doc for a named file (timetable.md, courses.md, campus_guide.md)
and search_campus_docs for broader questions.
If a tool returns status=error, explain what documents exist.
If the question is only about what class meets on a weekday,
call transfer_to_agent with agent_name "schedule_agent".
""",
    tools=docs_tools,
)

root_agent = LlmAgent(
    name="campus_router",
    model=pick_model(),
    description="SMIT Peshawar campus router for schedule and document questions.",
    instruction=(
        "You are the SMIT Peshawar campus router. "
        "Route schedule vs docs questions. "
        "Send timetable / class-time questions to schedule_agent. "
        "Send course-content, campus-guide, and document questions to docs_agent. "
        "Greetings and small talk you may answer yourself. "
        "Specialists may transfer_to_agent if the topic changes."
    ),
    sub_agents=[schedule_agent, docs_agent],
)

# Live / bidirectional kiosk mode. The CLI uses SSE when --stream is passed.
run_config = RunConfig(streaming_mode=StreamingMode.BIDI)
sse_run_config = RunConfig(streaming_mode=StreamingMode.SSE)
