# SMIT Peshawar · Google ADK Campus Assistant

Python code for every layer in `SMIT_Peshawar_ADK_Agentic_AI.pdf`. Each workshop step is a git branch. The `complete` branch is the full campus assistant with a CLI chat.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a Gemini API key in `.env` (`GOOGLE_API_KEY`). Get one at [Google AI Studio](https://aistudio.google.com/app/apikey).

## CLI chat

```bash
python chat.py
```

Type a message, then Enter. Commands inside the chat: `quit`, `reset`, `verbose`, `stream`.

```bash
python chat.py --step 2
python chat.py --stream
python chat.py --verbose
python chat.py -m "What class is on Monday?"
```

You can also use ADK's own runner:

```bash
adk run campus_assistant
```

## Branches (one per PDF step)

| Branch | PDF step | What it adds |
| --- | --- | --- |
| `step-01-what-is-adk` | 1 | `Agent` campus chatbot |
| `step-02-llm-agent-tools` | 2 | `LlmAgent` + `check_class_schedule` tool |
| `step-03-litellm` | 3 | Swappable model via LiteLLM |
| `step-04-mcp-tools` | 4 | MCP filesystem + custom `read_campus_doc` |
| `step-05-agent-garden` | 5 | RAG Q&A pattern (`build_rag_agent`) |
| `step-06-streaming` | 6 | SSE / BIDI run configs |
| `step-07-hierarchical-routing` | 7 | Router + `schedule_agent` / `docs_agent` |
| `step-08-delegation` | 8 | `transfer_to_agent` handoff |
| `step-09-error-handling` | 9 | try/except tools + verbose debug |
| `complete` | final | End-to-end campus assistant |

```bash
git checkout step-02-llm-agent-tools
python chat.py
```

On `complete`, `steps/01_what_is_adk` … `steps/09_error_handling` keep a snapshot of each layer.

## Try these prompts

- What class is on Monday?
- Is there a class on Sunday?
- Summarize the campus guide.
- Who do I ask about API keys?
- I asked about Monday's class — what is that session actually about?

## Model swap (Step 3)

In `.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=...
LITELLM_MODEL=openai/gpt-4o-mini
```

Or `LLM_PROVIDER=anthropic` with `ANTHROPIC_API_KEY`. Tools and instructions stay the same.

## MCP (Step 4)

Optional. Set `ENABLE_MCP=true` and have Node.js (`npx`) installed. The custom `read_campus_doc` tool works without MCP.
