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
