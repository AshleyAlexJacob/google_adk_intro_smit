# Step 3 — Model flexibility via LiteLLM

Branch: `step-03-litellm`  
PDF: campus_assistant.py — v3

Same agent and tools as Step 2. Only the `model=` line changes (`LLM_PROVIDER` in `.env`).

## Run

```bash
git checkout step-03-litellm
python chat.py
```

On `complete`: `python chat.py --step 3`

## Manual test scenarios

Use the **same prompts** as Step 2. The answers should still come from `check_class_schedule`.

| # | Setup | You type | Pass if |
| --- | --- | --- | --- |
| 1 | `LLM_PROVIDER=gemini` (default) | `What class is on Monday?` | Python Basics, 6 PM. |
| 2 | Same | `What class is on Friday?` | Project Lab, 6 PM. |
| 3 | Change `.env` to `LLM_PROVIDER=openai` and set `OPENAI_API_KEY` | `What class is on Tuesday?` | Still Agentic AI with Google ADK, 6 PM. Tools did not change. |
| 4 | `LLM_PROVIDER=anthropic` + `ANTHROPIC_API_KEY` | `Saturday workshop time?` | Weekend Workshop, 10 AM. |
| 5 | Missing OpenAI key while `LLM_PROVIDER=openai` | `python chat.py` | CLI exits with a missing-key message. |

Skip 3–4 if you only have a Gemini key. Scenario 1–2 are enough to pass Step 3.

## What must stay the same

- `check_class_schedule` docstring and return shape
- Agent name and campus persona
- Only `model=` / `LLM_PROVIDER` differs
