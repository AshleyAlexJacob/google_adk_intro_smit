"""Campus tools with try/except so a failed lookup never stalls the chat."""

from __future__ import annotations

from pathlib import Path

from campus_assistant.config import DOCS_DIR

CLASSES = {
    "Monday": "Python Basics, 6 PM",
    "Tuesday": "Agentic AI with Google ADK, 6 PM",
    "Wednesday": "Prompt Engineering, 6 PM",
    "Thursday": "Multi-Agent Systems, 6 PM",
    "Friday": "Project Lab, 6 PM",
    "Saturday": "Weekend Workshop, 10 AM",
}

_DAY_ALIASES = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Tues": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Thur": "Thursday",
    "Thurs": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday",
}


def check_class_schedule(day: str) -> dict:
    """Look up SMIT Peshawar classes for a given weekday.

    Args:
        day: Weekday name such as Monday or Tuesday.

    Returns:
        A dict with status=success and the class, or status=error.
    """
    try:
        normalized = day.strip().title()
        normalized = _DAY_ALIASES.get(normalized, normalized)
        return {"status": "success", "class": CLASSES[normalized]}
    except KeyError:
        return {
            "status": "error",
            "message": f"No class on {day}. Valid days: {', '.join(CLASSES)}",
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {"status": "error", "message": f"Schedule lookup failed: {exc}"}


def search_campus_docs(query: str) -> dict:
    """Search campus documents and return the most relevant snippets.

    Args:
        query: The student's question or keywords.

    Returns:
        Ranked document snippets to ground the answer.
    """
    try:
        terms = {token.lower() for token in query.replace("?", " ").split() if len(token) > 2}
        scored = []
        for path in sorted(DOCS_DIR.glob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            haystack = f"{path.name}\n{text}".lower()
            score = sum(haystack.count(term) for term in terms)
            scored.append((score, path.name, text))
        scored.sort(key=lambda row: row[0], reverse=True)
        hits = [
            {"file": filename, "snippet": text[:1200]}
            for score, filename, text in scored[:3]
            if score > 0
        ]
        if not hits:
            return {"status": "error", "message": "No matching campus documents."}
        return {"status": "success", "matches": hits}
    except Exception as exc:  # pragma: no cover - defensive
        return {"status": "error", "message": f"Search failed: {exc}"}


def read_campus_doc(filename: str) -> dict:
    """Read a campus document by file name, for example timetable.md.

    Args:
        filename: Document name inside the docs folder.

    Returns:
        File contents, or an error if the file is missing.
    """
    try:
        path = DOCS_DIR / Path(filename).name
        if not path.is_file():
            raise FileNotFoundError(filename)
        return {
            "status": "success",
            "filename": path.name,
            "content": path.read_text(encoding="utf-8"),
        }
    except FileNotFoundError:
        available = [p.name for p in DOCS_DIR.glob("*") if p.is_file()]
        return {
            "status": "error",
            "message": f"No document named {filename}. Available: {available}",
        }
    except OSError as exc:
        return {"status": "error", "message": f"Could not read {filename}: {exc}"}
