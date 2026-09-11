# Step 9 — Error handling and debugging

Branch: `step-09-error-handling`  
PDF: campus_assistant.py — v9

Tools catch errors and return `{ "status": "error", "message": "..." }`. The student chat must keep going.

## Run

```bash
git checkout step-09-error-handling
python chat.py --verbose
```

On `complete`: `python chat.py --step 9 --verbose`

## Manual test scenarios

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `Is there a class on Sunday?` | Tool `status=error` (or no Sunday class). Agent lists valid days (Mon–Sat). **Process does not crash.** |
| 2 | `What class is on Funday?` | Same: error status, helpful message. Then you can ask Monday and get Python Basics. |
| 3 | `Read secret.md` | Missing-file error; lists timetable.md, courses.md, campus_guide.md. |
| 4 | `What class is on Sunday?` then `OK, what about Monday?` | After the error, Monday still works. |
| 5 | `What class is on Monday?` | Still Python Basics, 6 PM (happy path unchanged). |
| 6 | Type `verbose` in the chat | Toggles tracing. Next question prints `[tool call]` / `[tool result]`. |
| 7 | `adk run --verbose` (optional) | Extra ADK logs; same Sunday behavior. |

## Fail this step if

- The CLI traceback-exits on Sunday
- The agent invents a Sunday class
- After an error, later questions stop working
