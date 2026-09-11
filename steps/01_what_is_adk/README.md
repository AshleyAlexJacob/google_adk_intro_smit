# Step 1 — What is ADK?

Branch: `step-01-what-is-adk`  
PDF: campus_assistant.py — v1

A model-agnostic `Agent` with no tools. It can chat, but it cannot look up the real timetable or campus docs.

## Run

```bash
git checkout step-01-what-is-adk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set GOOGLE_API_KEY
python chat.py
```

On `complete`: `python chat.py --step 1`

## Manual test scenarios

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `Assalam o Alaikum` | Friendly SMIT campus greeting; offers to help. |
| 2 | `Who are you?` | Identifies as the SMIT Peshawar campus assistant. |
| 3 | `Where is SMIT Peshawar?` | General campus answer is OK. There is **no docs tool** yet, so it may not know "Opposite Jan's Deli". |
| 4 | `What class is on Monday?` | Does **not** reliably say "Python Basics, 6 PM". No schedule tool — it should admit it does not have a timetable, or guess. |
| 5 | `Remember my name is Ali` then `What is my name?` | Follow-up works in the same session (conversation memory). |
| 6 | `reset` then `What is my name?` | New session; it should not still know "Ali". |
| 7 | `quit` | Process exits cleanly. |

## Negative checks

- Do **not** expect a tool call. `--verbose` should show no `check_class_schedule`.
- Do **not** expect grounded answers from `docs/timetable.md`.
