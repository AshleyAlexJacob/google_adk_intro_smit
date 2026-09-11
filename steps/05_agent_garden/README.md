# Step 5 — Agent Garden RAG Q&A pattern

Branch: `step-05-agent-garden`  
PDF: campus_assistant.py — v5

`build_rag_agent(corpus_path="./docs")` retrieves snippets before answering. Answers should be grounded in `docs/`.

## Run

```bash
git checkout step-05-agent-garden
python chat.py
```

On `complete`: `python chat.py --step 5`

## Manual test scenarios

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `Where is the campus?` | Opposite Jan's Deli, University Town, Peshawar. |
| 2 | `What are the student tips?` | Bring a laptop if you can; don't commit `.env`; `python chat.py`. |
| 3 | `Who handles schedule changes?` | Course coordinator. |
| 4 | `Who helps with ADK homework?` | Teaching assistant during Project Lab. |
| 5 | `What will we build in this module?` | Multi-agent campus assistant (from `courses.md`). |
| 6 | `When are instructor office hours?` | Thursday 5:00 PM – 6:00 PM. |
| 7 | `What is the weather in Karachi?` | Should **not** invent campus facts. Prefer "not in the documents" / I don't have that. |
| 8 | `Tell me something from the docs about LiteLLM.` | Mentions swapping the `model=` line. |

## Verbose

```bash
python chat.py --verbose -m "Where is the campus?"
```

Pass if `search_docs` runs **before** the final answer.
