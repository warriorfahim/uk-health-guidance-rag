"""Question answering for the HTTP API: retrieve, ask the LLM, return plain data (no web framework)."""
from collections.abc import Callable

from .answer import answer

NO_LLM_PREFIX = "No LLM available ("  # how llm.make_echo_generate starts its reply


def ask(question: str, retriever, generate: Callable[[str], str], k: int = 3) -> dict:
    """Return the answer and its numbered sources.

    `answer` is None when no LLM is usable, so a caller never mistakes the echoed prompt for an
    answer. The sources are returned either way.
    """
    hits = retriever.search(question, k=k)
    reply = answer(question, hits, generate)
    llm_used = not reply.startswith(NO_LLM_PREFIX)
    return {
        "answer": reply if llm_used else None,
        "llm_used": llm_used,
        "sources": [
            {"ref": i, "source": h["source"], "chunk_id": h["chunk_id"],
             "score": h["score"], "text": h["text"]}
            for i, h in enumerate(hits, start=1)
        ],
    }
