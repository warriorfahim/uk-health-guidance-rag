"""Build a grounded prompt and call an LLM of your choice."""
from collections.abc import Callable

SYSTEM_RULES = (
    "Answer the question using ONLY the numbered sources below. "
    "Cite sources like [1] after each claim. "
    "If the sources do not contain the answer, say you cannot answer from the provided guidance."
)


def build_prompt(question: str, hits: list[dict]) -> str:
    sources = "\n\n".join(f"[{i}] ({h['source']}) {h['text']}" for i, h in enumerate(hits, start=1))
    return f"{SYSTEM_RULES}\n\nSources:\n{sources}\n\nQuestion: {question}\nAnswer:"


def answer(question: str, hits: list[dict], generate: Callable[[str], str]) -> str:
    """`generate` takes a prompt string and returns the model's reply.

    Plug in any LLM here, for example a local open model or an API client.
    """
    return generate(build_prompt(question, hits))
