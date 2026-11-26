import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from ragdemo.api import create_app


class FakeRetriever:
    def search(self, query, k=5):
        return [{"source": "a.txt", "chunk_id": 0, "text": "Alpha.", "score": 0.9}][:k]


def client(retriever_factory=FakeRetriever, generate=lambda prompt: "Alpha [1]"):
    return TestClient(create_app(retriever_factory, lambda: generate))


def test_health():
    assert client().get("/health").json() == {"status": "ok"}


def test_ask_returns_answer_and_sources():
    response = client().post("/ask", json={"question": "What?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Alpha [1]"
    assert response.json()["sources"][0]["source"] == "a.txt"


@pytest.mark.parametrize("body", [{"question": "   "}, {"question": "x" * 501},
                                  {"question": "What?", "k": 0}, {"question": "What?", "k": 11}])
def test_ask_rejects_bad_input(body):
    assert client().post("/ask", json=body).status_code == 422


def test_missing_index_gives_503():
    def broken():
        raise FileNotFoundError("data/index.faiss")

    assert client(retriever_factory=broken).post("/ask", json={"question": "What?"}).status_code == 503


def test_llm_failure_gives_502():
    def fail(prompt):
        raise RuntimeError("boom")

    assert client(generate=fail).post("/ask", json={"question": "What?"}).status_code == 502
