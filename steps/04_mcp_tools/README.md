# Step 4 — Native MCP tools and a custom docs tool

Branch: `step-04-mcp-tools`  
PDF: campus_assistant.py — v4

Schedule tool **plus** `read_campus_doc` (and optional MCP filesystem over `./docs`).

## Run

```bash
git checkout step-04-mcp-tools
python chat.py
```

On `complete`: `python chat.py --step 4`

MCP is optional. Custom `read_campus_doc` works without Node. To try MCP: install Node.js, set `ENABLE_MCP=true` on `complete` (this step branch always constructs `McpToolset`; if `npx` is missing, docs still work via `read_campus_doc`).

## Manual test scenarios

### Schedule (tool still required)

| # | You type | Pass if |
| --- | --- | --- |
| 1 | `What class is on Monday?` | Python Basics, 6 PM. |
| 2 | `Saturday?` | Weekend Workshop, 10 AM. |

### Campus documents

| # | You type | Pass if |
| --- | --- | --- |
| 3 | `Summarize the campus guide.` | Mentions University Town / Jan's Deli, lab, prayer area, or help desk. |
| 4 | `Who do I ask about API keys?` | Instructor office hours, **Thursday 5 PM**. |
| 5 | `Where is the prayer area?` | Ground floor. |
| 6 | `What should I put in .env?` | Don't commit `.env`; keep API keys local. |
| 7 | `Read timetable.md and tell me Friday's session.` | Project Lab, 6:00 PM – 9:00 PM (from the file, not only the Python dict). |
| 8 | `List the docs you can read.` | timetable.md, courses.md, campus_guide.md. |
| 9 | `Read missing-file.md` | Error / "unknown document", lists available files. Chat continues. |

### Verbose

```bash
python chat.py --verbose -m "Who do I ask about API keys?"
```

Pass if you see `read_campus_doc` and/or an MCP `read_file` / `search_files` call.
