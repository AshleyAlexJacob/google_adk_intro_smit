"""Agent Garden-style RAG Q&A pattern, adapted for SMIT campus docs.

The workshop slide imports `google.adk.samples.rag_qa.build_rag_agent`.
Agent Garden is Google's library of ready-made agent patterns. This local
template keeps the same idea: start from RAG Q&A and point it at a corpus.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent

from campus_assistant.config import pick_model
from campus_assistant.tools import search_campus_docs


def build_rag_agent(corpus_path: str = "./docs", name: str = "docs_qa_agent") -> LlmAgent:
    """Build a retrieval-grounded Q&A agent over the campus document corpus."""
    _ = corpus_path  # corpus lives in campus_assistant.config.DOCS_DIR
    return LlmAgent(
        name=name,
        model=pick_model(),
        description="Answers SMIT campus questions using retrieved course documents.",
        instruction=(
            "You are the SMIT docs Q&A assistant. "
            "Always call search_campus_docs before answering questions about campus, "
            "timetable, or course content. Ground answers in the retrieved snippets. "
            "If nothing relevant is found, say so."
        ),
        tools=[search_campus_docs],
    )
