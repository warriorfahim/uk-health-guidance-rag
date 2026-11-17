from ragdemo.answer_check import describe_backend, format_entry, sample_rows


def test_sample_rows_one_per_source_and_repeatable():
    rows = [{"question": f"q{i}", "expected_source": f"s{i % 3}"} for i in range(9)]
    a = sample_rows(rows, 5, seed=1)
    assert a == sample_rows(rows, 5, seed=1)
    assert len(a) == 3 and len({r["expected_source"] for r in a}) == 3


def test_format_entry_flags_missing_expected_source():
    row = {"question": "Q?", "expected_source": "x.txt"}
    hits = [{"source": "y.txt"}]
    out = format_entry(1, "in-scope", row, "ans", hits)
    assert "retrieved in top 3: NO" in out and "ans" in out


def test_describe_backend(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    assert describe_backend() == "ollama (qwen2.5:7b)"
    monkeypatch.setenv("LLM_BACKEND", "none")
    assert describe_backend() == "none"
