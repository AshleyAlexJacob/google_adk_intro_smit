# SMIT Peshawar Course Notes — Google ADK

This module builds a Campus Assistant layer by layer with Google Agent Development Kit (ADK).

## What you will build

A multi-agent campus assistant that can:

- Answer friendly campus questions
- Look up the weekly class schedule
- Read course documents
- Route schedule vs docs questions to specialist agents
- Hand off a conversation with `transfer_to_agent`
- Recover from tool errors without crashing the chat

## Tools students should know

- `LlmAgent`: an agent that reasons with an LLM and can call tools
- LiteLLM: swap Gemini, OpenAI, or Anthropic by changing the `model=` line
- MCP: connect an agent to an external tool server (filesystem, database, custom)
- Agent Garden: start from a proven pattern such as RAG Q&A instead of writing retrieval from scratch
- `sub_agents`: hierarchical routing from a root agent to specialists
