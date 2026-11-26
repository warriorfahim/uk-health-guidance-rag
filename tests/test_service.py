from ragdemo.llm import make_echo_generate
from ragdemo.service import ask


class FakeRetriever:
    def search(self, query, k=5):
        hits = [{"source": "a.txt", "chunk_id": 0, "text": "Alpha.", "score": 0.9},
                {"source": "b.txt", "chunk_id": 3, "text": "Beta.", "score": 0.5}]
        return hits[:k]


def test_returns_answer_with_numbered_sources():
    result = ask("What?", FakeRetriever(), lambda prompt: "Alpha [1]", k=2)
    assert result["answer"] == "Alpha [1]"
    assert result["llm_used"] is True
    assert [(s["ref"], s["source"]) for s in result["sources"]] == [(1, "a.txt"), (2, "b.txt")]


def test_no_llm_gives_no_answer_but_keeps_sources():
    result = ask("What?", FakeRetriever(), make_echo_generate("LLM_BACKEND=none"), k=1)
    assert result["answer"] is None
    assert result["llm_used"] is False
    assert len(result["sources"]) == 1
