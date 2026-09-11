"""Step 5 — Agent Garden: start from a RAG Q&A pattern.

Matches campus_assistant.py — v5 in SMIT_Peshawar_ADK_Agentic_AI.pdf.

The slide imports `google.adk.samples.rag_qa`. Agent Garden is Google's
library of ready-made patterns (RAG, research, data analysis). This local
template follows the same idea: call build_rag_agent() and point it at a corpus.
"""

from pathlib import Path

from google.adk.agents import LlmAgent


def _corpus_dir(corpus_path: str) -> Path:
    path = Path(corpus_path)
    if path.is_dir():
        return path
    here = Path(__file__).resolve()
    for candidate in (here.parents[2] / "docs", Path.cwd() / "docs"):
        if candidate.is_dir():
            return candidate
    return path


def _load_corpus(corpus_path: str) -> list[tuple[str, str]]:
    docs = []
    folder = _corpus_dir(corpus_path)
    for path in sorted(folder.glob("*")):
        if path.suffix.lower() in {".md", ".txt"}:
            docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def build_rag_agent(corpus_path: str, name: str = "docs_qa_agent") -> LlmAgent:
    """Build a retrieval-grounded Q&A agent over a local document corpus."""
    documents = _load_corpus(corpus_path)

    def search_docs(query: str) -> dict:
        """Search campus documents and return the most relevant snippets.

        Args:
            query: The student's question or keywords.

        Returns:
            Ranked document snippets to ground the answer.
        """
        terms = {token.lower() for token in query.replace("?", " ").split() if len(token) > 2}
        scored = []
        for filename, text in documents:
            haystack = f"{filename}\n{text}".lower()
            score = sum(haystack.count(term) for term in terms) or (1 if not terms else 0)
            scored.append((score, filename, text))
        scored.sort(key=lambda row: row[0], reverse=True)
        hits = [
            {"file": filename, "snippet": text[:1200]}
            for score, filename, text in scored[:3]
            if score > 0
        ]
        if not hits:
            return {"status": "error", "message": "No matching campus documents."}
        return {"status": "success", "matches": hits}

    return LlmAgent(
        name=name,
        model="gemini-2.0-flash",
        description="Answers SMIT campus questions using retrieved course documents.",
        instruction=(
            "You are the SMIT docs Q&A assistant. "
            "Always call search_docs before answering questions about campus, "
            "timetable, or course content. Ground answers in the retrieved snippets. "
            "If nothing relevant is found, say so."
        ),
        tools=[search_docs],
    )


# Adapt the template instead of writing RAG by hand
docs_qa_agent = build_rag_agent(corpus_path="./docs", name="docs_qa_agent")
root_agent = docs_qa_agent
