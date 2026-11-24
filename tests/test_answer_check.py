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


def test_parse_args_retrieval_defaults():
    from ragdemo.answer_check import parse_args
    from ragdemo.index import DEFAULT_MODEL

    args = parse_args([])
    assert args.chunks == "data/chunks.jsonl"
    assert args.index == "data/index.faiss"
    assert args.model == DEFAULT_MODEL


def test_parse_args_retrieval_overrides():
    from ragdemo.answer_check import parse_args

    args = parse_args(["--chunks", "a.jsonl", "--index", "b.faiss", "--model", "m", "--delay", "10"])
    assert (args.chunks, args.index, args.model, args.delay) == ("a.jsonl", "b.faiss", "m", 10.0)


def test_format_entry_shows_finish_reason_and_tokens():
    info = {"finish_reason": "length", "usage": {
        "prompt_tokens": 10, "completion_tokens": 400,
        "completion_tokens_details": {"reasoning_tokens": 390}}}
    out = format_entry(1, "out-of-scope", {"question": "Q?"}, "ans", [{"source": "y.txt"}], info)
    assert "- Finish reason: length" in out
    assert "- Tokens: prompt 10, completion 400, reasoning 390" in out


def test_parse_args_max_tokens():
    from ragdemo.answer_check import parse_args

    assert parse_args([]).max_tokens == 400
    assert parse_args(["--max-tokens", "1500"]).max_tokens == 1500
