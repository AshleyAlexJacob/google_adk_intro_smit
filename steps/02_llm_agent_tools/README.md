# Step 2 — LlmAgent, tools, and orchestration

Branch: `step-02-llm-agent-tools`  
PDF: campus_assistant.py — v2

`LlmAgent` plus `check_class_schedule`. ADK decides when to call the tool from the docstring.

## Run

```bash
git checkout step-02-llm-agent-tools
python chat.py
python chat.py --verbose -m "What class is on Monday?"
```

On `complete`: `python chat.py --step 2`

## Manual test scenarios

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `What class is on Monday?` | **Python Basics, 6 PM**. Verbose shows `check_class_schedule` with `day` ≈ Monday. |
| 2 | `What do we study on Tuesday?` | **Agentic AI with Google ADK, 6 PM**. |
| 3 | `Wednesday timetable please` | **Prompt Engineering, 6 PM**. |
| 4 | `What's on Thu?` | **Multi-Agent Systems, 6 PM** (or the agent maps Thu → Thursday before calling the tool). |
| 5 | `Friday lab time?` | **Project Lab, 6 PM**. |
| 6 | `Is there class on Saturday?` | **Weekend Workshop, 10 AM**. |
| 7 | `Is there a class on Sunday?` | Tool returns `"class": "None"`. Agent says there is no class / campus is closed. Chat must **not** crash. |
| 8 | `Hi, can you help me?` | Greeting without a tool call is OK. |
| 9 | `What class is on Monday?` then `What about Tuesday?` | Second turn still uses the tool; Tuesday is Agentic AI. |
| 10 | `Where is the prayer area?` | No docs tool yet. Agent should not pretend it read `campus_guide.md`. |

## Verbose check

```bash
python chat.py --verbose -m "What class is on Monday?"
```

Look for `[tool call] check_class_schedule(...)`.
