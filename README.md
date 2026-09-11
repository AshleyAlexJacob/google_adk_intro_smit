# SMIT Peshawar · Google ADK Campus Assistant

Hands-on code for **SMIT Peshawar Agentic AI** — *Google Agent Development Kit (ADK): Building a Multi-Agent Campus Assistant, Layer by Layer*.

This repo follows `SMIT_Peshawar_ADK_Agentic_AI.pdf`. You start with a simple campus chatbot and add tools, LiteLLM, MCP, RAG, streaming, routing, delegation, and error handling until you have one working assistant.

Checkout **`complete`** for the full app and CLI chat:

```bash
git checkout complete
```

---

## What you will build

A **Campus Assistant** for SMIT Peshawar students that can:

- Chat in a friendly campus voice
- Look up the weekly class schedule
- Read course documents (`docs/`)
- Route timetable vs document questions to specialist agents
- Hand off a conversation with `transfer_to_agent`
- Recover from tool errors without crashing the chat

The interface is a **pure Python CLI** (`chat.py`). No web UI is required.

---

## Setup

You need Python 3.10+ and a Gemini API key.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and set:

```
GOOGLE_API_KEY=your_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.0-flash
```

Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

Never commit `.env`.

---

## CLI chat

From the project root, with the virtualenv active:

```bash
python chat.py
```

Example session:

```text
============================================================
 SMIT Peshawar · Campus Assistant
 Agent: campus_router
 Commands: quit | reset | verbose | stream
============================================================

You: What class is on Monday?
Assistant: Monday is Python Basics at 6 PM.
```

### Commands inside the chat

| Command | What it does |
| --- | --- |
| `quit` / `exit` / `q` | Leave the chat |
| `reset` | Start a new conversation (clears memory) |
| `verbose` | Toggle tool-call / event tracing (Step 9 debugging) |
| `stream` | Toggle token-by-token SSE printing (Step 6) |

### Useful flags

```bash
python chat.py -m "What class is on Monday?"
python chat.py --step 2
python chat.py --stream
python chat.py --verbose
python chat.py --step 7 --verbose -m "Summarize the campus guide"
```

| Flag | Meaning |
| --- | --- |
| `-m` / `--message` | Send one message and exit |
| `--step N` | Chat with workshop step `1`–`9` instead of the assembled router |
| `--stream` | Print tokens as they arrive (`StreamingMode.SSE`) |
| `--verbose` | Print tool calls and ADK events |

You can also use ADK's own runner:

```bash
adk run campus_assistant
adk web
```

---

## Manual test scenarios

Each branch has its own README with queries and pass/fail checks:

| Branch | Test guide |
| --- | --- |
| `main` | This file — overview only; no chat to run |
| `step-01-what-is-adk` | [steps/01_what_is_adk/README.md](steps/01_what_is_adk/README.md) |
| `step-02-llm-agent-tools` | [steps/02_llm_agent_tools/README.md](steps/02_llm_agent_tools/README.md) |
| `step-03-litellm` | [steps/03_litellm/README.md](steps/03_litellm/README.md) |
| `step-04-mcp-tools` | [steps/04_mcp_tools/README.md](steps/04_mcp_tools/README.md) |
| `step-05-agent-garden` | [steps/05_agent_garden/README.md](steps/05_agent_garden/README.md) |
| `step-06-streaming` | [steps/06_streaming/README.md](steps/06_streaming/README.md) |
| `step-07-hierarchical-routing` | [steps/07_hierarchical_routing/README.md](steps/07_hierarchical_routing/README.md) |
| `step-08-delegation` | [steps/08_delegation/README.md](steps/08_delegation/README.md) |
| `step-09-error-handling` | [steps/09_error_handling/README.md](steps/09_error_handling/README.md) |
| `complete` | End-to-end table below |

Stay on `complete` and target a layer with `--step`:

```bash
python chat.py --step 2 --verbose -m "What class is on Monday?"
```

### End-to-end (`complete` / `python chat.py`)

Run these in order in **one** session unless a row says `reset`.

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `Assalam o Alaikum` | Friendly campus greeting from `campus_router`. |
| 2 | `What class is on Monday?` | Python Basics, 6 PM (`schedule_agent`). |
| 3 | `What is that session actually about?` | Course/ADK context from docs (`docs_agent` / transfer). |
| 4 | `Summarize the campus guide.` | University Town, Jan's Deli, lab / prayer area / help desk. |
| 5 | `Who do I ask about API keys?` | Instructor office hours, Thursday 5 PM. |
| 6 | `Is there a class on Sunday?` | No class; lists valid days; **does not crash**. |
| 7 | `OK, what about Friday?` | Project Lab, 6 PM (chat recovered after the error). |
| 8 | `Where is the prayer area?` | Ground floor. |
| 9 | `reset` then `What is that session about?` | No leftover Monday context. |
| 10 | `quit` | Clean exit. |

Flags to mix in:

```bash
python chat.py --verbose
python chat.py --stream -m "What class is on Tuesday?"
python chat.py --step 1 -m "Who are you?"
python chat.py --step 9 --verbose -m "Is there a class on Sunday?"
```

### Schedule answer key

| Day | Class |
| --- | --- |
| Monday | Python Basics, 6 PM |
| Tuesday | Agentic AI with Google ADK, 6 PM |
| Wednesday | Prompt Engineering, 6 PM |
| Thursday | Multi-Agent Systems, 6 PM |
| Friday | Project Lab, 6 PM |
| Saturday | Weekend Workshop, 10 AM |
| Sunday | No class (error / closed) |

---

## Project layout

```text
google_adk_intro/
├── SMIT_Peshawar_ADK_Agentic_AI.pdf   # workshop slides
├── chat.py                            # Python CLI chat
├── requirements.txt
├── .env.example
├── campus_assistant/                  # assembled app (complete branch)
│   ├── agent.py                       # campus_router + sub-agents
│   ├── tools.py                       # schedule + docs tools
│   ├── config.py                      # model / path helpers
│   ├── mcp_docs.py                    # optional MCP filesystem
│   └── garden/rag_qa.py               # Agent Garden-style RAG template
├── docs/                              # campus corpus
│   ├── timetable.md
│   ├── courses.md
│   └── campus_guide.md
└── steps/                             # snapshot of each PDF layer
    ├── 01_what_is_adk/
    ├── 02_llm_agent_tools/
    ├── 03_litellm/
    ├── 04_mcp_tools/
    ├── 05_agent_garden/
    ├── 06_streaming/
    ├── 07_hierarchical_routing/
    ├── 08_delegation/
    └── 09_error_handling/
```

On `complete`, `python chat.py` runs `campus_assistant/agent.py`.  
`python chat.py --step 4` loads `steps/04_mcp_tools/agent.py`.

---

## Git branches (one per PDF step)

Each step is its own branch. Later steps build on earlier ones. `complete` is the end-to-end solution.

| Branch | PDF | What it adds |
| --- | --- | --- |
| `main` | — | Course scaffold only (README, requirements, PDF) |
| `step-01-what-is-adk` | Step 1 | `Agent` campus chatbot |
| `step-02-llm-agent-tools` | Step 2 | `LlmAgent` + `check_class_schedule` tool |
| `step-03-litellm` | Step 3 | Swappable model via LiteLLM |
| `step-04-mcp-tools` | Step 4 | MCP filesystem + custom `read_campus_doc` |
| `step-05-agent-garden` | Step 5 | RAG Q&A pattern (`build_rag_agent`) |
| `step-06-streaming` | Step 6 | SSE / BIDI run configs |
| `step-07-hierarchical-routing` | Step 7 | Router + `schedule_agent` / `docs_agent` |
| `step-08-delegation` | Step 8 | `transfer_to_agent` handoff |
| `step-09-error-handling` | Step 9 | try/except tools + verbose debug |
| **`complete`** | Final | Full campus assistant — **start here** |

Walk a single layer:

```bash
git checkout step-02-llm-agent-tools
python chat.py
```

Stay on `complete` and jump between snapshots:

```bash
git checkout complete
python chat.py --step 1
python chat.py --step 9
```

---

## Step notes (mapped to the PDF)

### 1. What is ADK?

Google ADK is an open-source, model-agnostic framework. The same code path can be a simple chatbot or a multi-agent system.

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="campus_assistant",
    model="gemini-2.0-flash",
    instruction="Friendly SMIT campus assistant.",
)
```

### 2. LlmAgent, tools, and orchestration

A tool is a normal Python function with a clear docstring. ADK decides when to call it.

```python
def check_class_schedule(day: str) -> dict:
    """Look up SMIT Peshawar classes for a given weekday."""
    ...

root_agent = LlmAgent(
    name="campus_assistant",
    model="gemini-2.0-flash",
    tools=[check_class_schedule],
)
```

### 3. Model flexibility via LiteLLM

Only the `model=` line changes. Tools and instructions stay the same.

In `.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=...
LITELLM_MODEL=openai/gpt-4o-mini
```

Or `LLM_PROVIDER=anthropic` with `ANTHROPIC_API_KEY`. Default is Gemini.

### 4. Native MCP + custom tools

MCP connects any compatible tool server (filesystem, database, custom) with a few lines. This repo also ships a custom `read_campus_doc` tool so docs work without Node.

Optional MCP:

1. Install Node.js (`npx`)
2. Set `ENABLE_MCP=true` in `.env`

### 5. Agent Garden

Agent Garden is Google's library of ready-made patterns (RAG Q&A, research, data analysis). The slide import `google.adk.samples.rag_qa` is that idea. Here it is a local template:

```python
from campus_assistant.garden.rag_qa import build_rag_agent

docs_qa_agent = build_rag_agent(corpus_path="./docs", name="docs_qa_agent")
```

### 6. Bidirectional audio and video streaming

Same agent and tools — a different run mode.

- Text CLI: `python chat.py --stream` uses `StreamingMode.SSE`
- Live kiosk (audio/video): `RunConfig(streaming_mode=StreamingMode.BIDI)` plus `runner.run_live()`

### 7. Hierarchical structures and routing

A root agent holds `sub_agents` instead of only tools. It reads the question and routes it.

- `schedule_agent` — timetable
- `docs_agent` — course / campus documents
- `campus_router` — sends traffic to the right specialist

### 8. Agent-to-agent delegation

Delegation hands off the **whole turn**, not just an answer. ADK's `transfer_to_agent` carries conversation state automatically. No manual copying of chat history.

### 9. Error handling and debugging

Catch errors in tools, return `{ "status": "error", "message": "..." }`, and let the agent keep talking.

```bash
python chat.py --verbose
# or: adk run --verbose
```

Ask *Is there a class on Sunday?* — the tool returns an error status instead of crashing.

### Final assembly

The `complete` agent layers all of the above:

- Router (`campus_router`)
- Two focused sub-agents
- Docs tools (custom + optional MCP)
- LiteLLM-ready `model=` slot
- try/except in every tool

---

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `GOOGLE_API_KEY` | — | Gemini key (required unless you use another provider) |
| `GOOGLE_GENAI_USE_VERTEXAI` | `FALSE` | Use AI Studio keys, not Vertex |
| `LLM_PROVIDER` | `gemini` | `gemini`, `openai`, or `anthropic` |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model id |
| `LITELLM_MODEL` | `openai/gpt-4o-mini` | LiteLLM model string |
| `OPENAI_API_KEY` | — | Required when `LLM_PROVIDER=openai` |
| `ANTHROPIC_API_KEY` | — | Required when `LLM_PROVIDER=anthropic` |
| `ENABLE_MCP` | unset | Set `true` to attach the MCP filesystem server |

---

## Troubleshooting

**`Missing API key`**  
Copy `.env.example` to `.env` and set `GOOGLE_API_KEY`.

**`ModuleNotFoundError: google.adk`**  
Activate `.venv` and run `pip install -r requirements.txt`.

**MCP / `npx` errors**  
Leave `ENABLE_MCP` unset. `read_campus_doc` and `search_campus_docs` still work.

**`Step N is not on this branch`**  
`--step` snapshots live on `complete`. Either `git checkout complete` or check out that step branch and run `python chat.py` with no `--step`.

**Sunday / unknown day**  
That is Step 9 on purpose. The tool returns `status=error` and the agent should explain valid days.

---

## Course

SMIT Peshawar · Agentic AI · *96 Hours to change your career.*
Next module in the slides: Agent Evaluation & Observability.
