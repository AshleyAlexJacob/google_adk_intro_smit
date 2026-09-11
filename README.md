# SMIT Peshawar · Google ADK Campus Assistant

Hands-on code for **SMIT Peshawar Agentic AI** — *Google Agent Development Kit (ADK): Building a Multi-Agent Campus Assistant, Layer by Layer*.

This is the **`main`** branch: course scaffold only (this README, `requirements.txt`, `.env.example`, and the workshop PDF). There is **no chat app on `main`**. Check out a step branch or `complete` to run tests.

```bash
git checkout complete          # full assistant — start here to chat
git checkout step-02-llm-agent-tools
```

Slides: `SMIT_Peshawar_ADK_Agentic_AI.pdf`

---

## Setup (after you check out a code branch)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # set GOOGLE_API_KEY
python chat.py
```

Get a Gemini key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Branches and where to test

| Branch | README on that branch | What you are testing |
| --- | --- | --- |
| `main` | this file | Overview only |
| `step-01-what-is-adk` | `README.md` | Chat with no tools |
| `step-02-llm-agent-tools` | `README.md` | `check_class_schedule` |
| `step-03-litellm` | `README.md` | Same tools, swapped model |
| `step-04-mcp-tools` | `README.md` | Docs + optional MCP |
| `step-05-agent-garden` | `README.md` | RAG over `docs/` |
| `step-06-streaming` | `README.md` | `python chat.py --stream` |
| `step-07-hierarchical-routing` | `README.md` | Router → specialists |
| `step-08-delegation` | `README.md` | `transfer_to_agent` |
| `step-09-error-handling` | `README.md` | Sunday / missing file, no crash |
| `complete` | `README.md` + `steps/*/README.md` | End-to-end campus assistant |

On `complete` you can also run a snapshot without changing branch:

```bash
git checkout complete
python chat.py --step 2 --verbose -m "What class is on Monday?"
```

---

## Manual test scenarios (all steps)

Use these after `git checkout <branch>`. Expected schedule:

| Day | Class |
| --- | --- |
| Monday | Python Basics, 6 PM |
| Tuesday | Agentic AI with Google ADK, 6 PM |
| Wednesday | Prompt Engineering, 6 PM |
| Thursday | Multi-Agent Systems, 6 PM |
| Friday | Project Lab, 6 PM |
| Saturday | Weekend Workshop, 10 AM |
| Sunday | No class |

### Step 1 — `step-01-what-is-adk`

| You type | Pass if |
| --- | --- |
| `Assalam o Alaikum` | Friendly SMIT greeting |
| `Who are you?` | Campus assistant persona |
| `What class is on Monday?` | Does **not** reliably know Python Basics (no tool yet) |
| `Remember my name is Ali` then `What is my name?` | Remembers in-session |
| `reset` then `What is my name?` | Forgets Ali |

### Step 2 — `step-02-llm-agent-tools`

| You type | Pass if |
| --- | --- |
| `What class is on Monday?` | Python Basics, 6 PM (tool call) |
| `What do we study on Tuesday?` | Agentic AI with Google ADK, 6 PM |
| `Is there a class on Sunday?` | No class; chat does not crash |
| `python chat.py --verbose -m "What class is on Monday?"` | Shows `check_class_schedule` |

### Step 3 — `step-03-litellm`

Same prompts as Step 2. Then set `LLM_PROVIDER=openai` (or `anthropic`) in `.env` and ask `What class is on Tuesday?` — still Agentic AI, 6 PM.

### Step 4 — `step-04-mcp-tools`

| You type | Pass if |
| --- | --- |
| `What class is on Monday?` | Python Basics, 6 PM |
| `Summarize the campus guide.` | University Town / Jan's Deli / lab or prayer area |
| `Who do I ask about API keys?` | Instructor, Thursday 5 PM |
| `Where is the prayer area?` | Ground floor |
| `Read missing-file.md` | Error + lists real docs; chat continues |

### Step 5 — `step-05-agent-garden`

| You type | Pass if |
| --- | --- |
| `Where is the campus?` | Opposite Jan's Deli, University Town |
| `Who handles schedule changes?` | Course coordinator |
| `What is the weather in Karachi?` | Not invented from campus docs |
| `--verbose` | `search_docs` runs before the answer |

### Step 6 — `step-06-streaming`

```bash
python chat.py --stream -m "What class is on Monday?"
```

Pass if the answer is Python Basics, 6 PM and output streams (or prints as a streamed block).

### Step 7 — `step-07-hierarchical-routing`

| You type | Pass if (`--verbose`) |
| --- | --- |
| `What class is on Monday?` | `schedule_agent` |
| `Summarize the campus guide.` | `docs_agent` |
| `Assalam o Alaikum` | Router may answer itself |

### Step 8 — `step-08-delegation`

Do **not** `reset` between the two lines.

| Conversation | Pass if |
| --- | --- |
| `What class is on Monday?` then `What is that session actually about?` | Handoff to docs / ADK module context |
| `Summarize the campus guide.` then `What time is Friday class?` | Handoff to schedule; Project Lab, 6 PM |
| `Who do I ask about API keys?` then `And what class is that day?` | Thursday office hours → Multi-Agent Systems |

### Step 9 — `step-09-error-handling`

| You type | Pass if |
| --- | --- |
| `Is there a class on Sunday?` | Error status, valid days listed, **no crash** |
| Then `OK, what about Monday?` | Python Basics, 6 PM |
| `Read secret.md` | Missing file, lists available docs |

### Complete — `complete`

Run in **one** session:

1. `Assalam o Alaikum`
2. `What class is on Monday?`
3. `What is that session actually about?`
4. `Summarize the campus guide.`
5. `Who do I ask about API keys?`
6. `Is there a class on Sunday?`
7. `OK, what about Friday?`
8. `Where is the prayer area?`
9. `reset` then `What is that session about?`
10. `quit`

Pass if schedule, docs, handoff, and error recovery all work. Details: `git checkout complete` and read that branch's `README.md`.

---

## Course

SMIT Peshawar · Agentic AI · *96 Hours to change your career.*
Next module in the slides: Agent Evaluation & Observability.
