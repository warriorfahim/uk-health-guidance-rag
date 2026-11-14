import pytest

from ragdemo.llm import make_hf_generate


def test_missing_token_raises(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="HF_TOKEN"):
        make_hf_generate()
