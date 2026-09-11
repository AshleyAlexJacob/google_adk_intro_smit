# Step 7 — Hierarchical structures and routing

Branch: `step-07-hierarchical-routing`  
PDF: campus_assistant.py — v7

`campus_router` sends timetable questions to `schedule_agent` and document questions to `docs_agent`.

## Run

```bash
git checkout step-07-hierarchical-routing
python chat.py --verbose
```

On `complete`: `python chat.py --step 7 --verbose`

## Manual test scenarios

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `Assalam o Alaikum` | Router may answer itself; no specialist required. |
| 2 | `What class is on Monday?` | Python Basics, 6 PM. Verbose author is **`schedule_agent`** (or a transfer to it). |
| 3 | `Thursday evening class?` | Multi-Agent Systems, 6 PM via schedule agent. |
| 4 | `Summarize the campus guide.` | Facilities / location from docs. Verbose author is **`docs_agent`**. |
| 5 | `Who do I ask about API keys?` | Thursday 5 PM, instructor. Routed to docs. |
| 6 | `Where is the prayer area?` | Ground floor, via docs agent. |
| 7 | `What class is on Monday and where is campus?` | Either two specialist turns, or one agent covering both after routing. Both facts should appear: Python Basics 6 PM **and** University Town / Jan's Deli. |

## Routing check

```bash
python chat.py --verbose -m "What class is on Tuesday?"
python chat.py --verbose -m "Who handles schedule changes?"
```

- First: `schedule_agent` + `check_class_schedule`
- Second: `docs_agent` + `read_campus_doc` (course coordinator)
