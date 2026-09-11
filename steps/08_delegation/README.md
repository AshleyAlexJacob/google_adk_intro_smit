# Step 8 — Agent-to-agent delegation

Branch: `step-08-delegation`  
PDF: campus_assistant.py — v8

Specialists can `transfer_to_agent` and ADK carries conversation state. No manual history copying.

## Run

```bash
git checkout step-08-delegation
python chat.py --verbose
```

On `complete`: `python chat.py --step 8 --verbose`

Do **not** type `reset` between the two lines of a handoff scenario.

## Manual test scenarios

| # | Conversation | Pass if |
| --- | --- | --- |
| 1 | `What class is on Monday?` then `What is that session actually about?` | First answer: Python Basics, 6 PM. Second: course-content / ADK module context from docs. Verbose shows `transfer_to_agent` → `docs_agent` (or the docs agent answering the follow-up). |
| 2 | `Summarize the campus guide.` then `What time is Friday class?` | First: campus facilities. Second: Project Lab, 6 PM via `schedule_agent`. |
| 3 | `Who do I ask about API keys?` then `And what class is that day?` | API keys → Thursday 5 PM office hours. Follow-up → Thursday class is **Multi-Agent Systems, 6 PM**. |
| 4 | `What class is on Tuesday?` then `Who helps with homework for that?` | Tuesday = Agentic AI / ADK. Homework → teaching assistant during Project Lab. |
| 5 | `reset` then `What is that session about?` | No leftover Monday context. Agent asks which session, or says it doesn't know. |

## Verbose

Look for `transfer_to_agent` / a change in `author=` from `schedule_agent` to `docs_agent` (or the reverse) **in the same session**.
