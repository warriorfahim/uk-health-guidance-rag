import argparse

from ragdemo.evaluate import parse_args
from ragdemo.index import DEFAULT_MODEL, add_model_args


def test_add_model_args_defaults():
    parser = argparse.ArgumentParser()
    add_model_args(parser)
    args = parser.parse_args([])
    assert args.model == DEFAULT_MODEL
    assert args.index == "data/index.faiss"


def test_add_model_args_overrides():
    parser = argparse.ArgumentParser()
    add_model_args(parser)
    args = parser.parse_args(["--model", "BAAI/bge-small-en-v1.5", "--index", "data/index_bge.faiss"])
    assert args.model == "BAAI/bge-small-en-v1.5"
    assert args.index == "data/index_bge.faiss"


def test_evaluate_parse_args_keeps_misses_flag():
    args = parse_args(["--misses"])
    assert args.misses is True
    assert args.model == DEFAULT_MODEL
    assert parse_args([]).misses is False


def test_evaluate_parse_args_model_and_index():
    args = parse_args(["--model", "m", "--index", "i.faiss"])
    assert (args.model, args.index) == ("m", "i.faiss")


def test_query_prefix_option_is_opt_in():
    parser = argparse.ArgumentParser()
    add_model_args(parser)
    assert "query_prefix" not in vars(parser.parse_args([]))
    parser = argparse.ArgumentParser()
    add_model_args(parser, query_prefix=True)
    assert parser.parse_args([]).query_prefix == ""
    assert parser.parse_args(["--query-prefix", "Q: "]).query_prefix == "Q: "


def test_evaluate_parse_args_query_prefix():
    assert parse_args(["--query-prefix", "Q: "]).query_prefix == "Q: "


def test_chunks_option_default_and_override():
    parser = argparse.ArgumentParser()
    add_model_args(parser)
    assert parser.parse_args([]).chunks == "data/chunks.jsonl"
    assert parser.parse_args(["--chunks", "data/chunks_400.jsonl"]).chunks == "data/chunks_400.jsonl"
