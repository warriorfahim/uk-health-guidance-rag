import pytest

from ragdemo.llm import make_hf_generate, make_openrouter_generate


def test_missing_token_raises(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="HF_TOKEN"):
        make_hf_generate()


def test_unknown_backend_raises(monkeypatch):
    from ragdemo.llm import make_generate

    monkeypatch.setenv("LLM_BACKEND", "nope")
    with pytest.raises(RuntimeError, match="LLM_BACKEND"):
        make_generate()


def test_falls_back_to_echo_without_ollama(monkeypatch):
    from ragdemo import llm

    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.setattr(llm, "ollama_available", lambda *a, **k: False)
    assert "Ollama is not running" in llm.make_generate()("PROMPT")


def test_hf_without_token_falls_back(monkeypatch):
    from ragdemo import llm

    monkeypatch.setenv("LLM_BACKEND", "hf")
    monkeypatch.delenv("HF_TOKEN", raising=False)
    out = llm.make_generate()("PROMPT")
    assert "HF_TOKEN is not set" in out and "PROMPT" in out


def test_openrouter_without_key_falls_back(monkeypatch):
    from ragdemo import llm

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = llm.make_generate("openrouter")("PROMPT")
    assert "OPENROUTER_API_KEY is not set" in out and "PROMPT" in out


def test_openrouter_missing_key_raises(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        make_openrouter_generate()


def test_openrouter_parses_response_and_sends_auth(monkeypatch):
    import io
    import json

    from ragdemo import llm

    seen = {}

    def fake_urlopen(req, timeout=None):
        seen["auth"] = req.get_header("Authorization")
        seen["body"] = json.loads(req.data)
        return io.BytesIO(json.dumps({"choices": [{"message": {"content": " hi "}}]}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    out = make_openrouter_generate(api_key="k", model="m")("PROMPT")
    assert out == "hi"
    assert seen["auth"] == "Bearer k" and seen["body"]["model"] == "m"


def test_openrouter_empty_answer_raises(monkeypatch):
    import io
    import json

    from ragdemo import llm

    monkeypatch.setattr(
        llm.urllib.request,
        "urlopen",
        lambda req, timeout=None: io.BytesIO(json.dumps({"choices": []}).encode()),
    )
    with pytest.raises(RuntimeError, match="empty"):
        make_openrouter_generate(api_key="k")("PROMPT")
