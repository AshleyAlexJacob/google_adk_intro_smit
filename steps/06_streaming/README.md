# Step 6 — Bidirectional audio and video streaming

Branch: `step-06-streaming`  
PDF: campus_assistant.py — v6

Same campus agent and schedule tool. Run mode changes: SSE for the text CLI, BIDI for a live kiosk.

## Run

```bash
git checkout step-06-streaming
python chat.py --stream
python chat.py --stream -m "What class is on Monday?"
```

On `complete`: `python chat.py --step 6 --stream`

## Manual test scenarios

| # | How | You type | Pass if |
| --- | --- | --- | --- |
| 1 | `python chat.py --stream` | `What class is on Monday?` | Python Basics, 6 PM. Tokens appear as they arrive (or as one streamed block). |
| 2 | Same | `Keep it short: Tuesday class?` | Short, spoken-style answer; Agentic AI with Google ADK. |
| 3 | Interactive, then type `stream` | Toggle on/off | Prompt confirms `Stream: True/False`. |
| 4 | Without `--stream` | `Friday?` | Full answer still correct (Project Lab). Streaming is optional. |
| 5 | `python chat.py --verbose --stream` | `Saturday workshop?` | Tool call still happens; Weekend Workshop, 10 AM. |

## What this step does **not** require

True microphone/camera BIDI needs `runner.run_live()` and a live Gemini model. The CLI proves the **same agent + different `RunConfig`**. Seeing SSE output is enough to pass the text path.
