"""Manual answer-quality check: run questions through the full pipeline and save a report.

Runs every question in eval/out_of_scope_questions.csv plus a sample from
eval/eval_questions.csv through retrieval (top 3, as in the app) and the LLM, then writes
results/answer_check.md for you to read and mark.

    python -m ragdemo.answer_check                 # 6 out-of-scope + 6 sampled questions
    python -m ragdemo.answer_check --sample 8 --seed 1
    $env:LLM_BACKEND = "openrouter"                # optional: pick another backend first
    python -m ragdemo.answer_check --chunks data/chunks_400.jsonl --index data/index_400.faiss
"""
import argparse
import csv
import os
import random
import time
from datetime import date
from pathlib import Path

from .index import add_model_args

K = 3  # same number of chunks the Streamlit app uses


def read_rows(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sample_rows(rows: list[dict], n: int, seed: int = 0) -> list[dict]:
    """Pick up to n rows, at most one per expected source, in a repeatable random order."""
    shuffled = rows[:]
    random.Random(seed).shuffle(shuffled)
    picked, seen = [], set()
    for row in shuffled:
        if row["expected_source"] in seen:
            continue
        seen.add(row["expected_source"])
        picked.append(row)
        if len(picked) == n:
            break
    return picked


def describe_backend() -> str:
    """Name the backend and model that `make_generate()` will use, for the report header."""
    from . import llm

    backend = os.environ.get("LLM_BACKEND", "ollama").lower()
    models = {
        "ollama": os.environ.get("OLLAMA_MODEL") or llm.OLLAMA_MODEL,
        "openrouter": os.environ.get("OPENROUTER_MODEL") or llm.OPENROUTER_DEFAULT_MODEL,
        "hf": os.environ.get("HF_MODEL") or llm.DEFAULT_MODEL,
    }
    return f"{backend} ({models[backend]})" if backend in models else backend


def run_question(question: str, retriever, generate) -> tuple[str, list[dict]]:
    """Return (answer or error text, retrieved hits) for one question."""
    from .answer import answer

    hits = retriever.search(question, k=K)
    try:
        return answer(question, hits, generate), hits
    except Exception as exc:  # noqa: BLE001 - record any backend failure in the report
        return f"ERROR from LLM: {exc}", hits


def format_info(info: dict) -> list[str]:
    """Report lines for the finish reason and token usage, if the backend recorded them."""
    lines = []
    if info.get("finish_reason"):
        lines.append(f"- Finish reason: {info['finish_reason']}")
    usage = info.get("usage") or {}
    reasoning = (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")
    counts = [("prompt", usage.get("prompt_tokens")), ("completion", usage.get("completion_tokens")),
              ("reasoning", reasoning)]
    shown = ", ".join(f"{name} {n}" for name, n in counts if n is not None)
    if shown:
        lines.append(f"- Tokens: {shown}")
    return lines


def format_entry(number: int, kind: str, row: dict, reply: str, hits: list[dict],
                 info: dict | None = None) -> str:
    lines = [f"### {number}. {row['question']}", "", f"- Type: {kind}"]
    if kind == "in-scope":
        expected = row["expected_source"]
        found = any(h["source"] == expected for h in hits)
        lines.append(f"- Expected source: `{expected}` (retrieved in top {K}: {'yes' if found else 'NO'})")
    else:
        lines.append(f"- Note: {row.get('note', '')}")
    lines.append("- Retrieved: " + ", ".join(f"[{i}] `{h['source']}`" for i, h in enumerate(hits, 1)))
    lines += format_info(info or {}) + [""]
    lines += ["**Answer:**", "", reply, ""]
    if kind == "in-scope":
        lines += ["- Correct? (yes/no/partly):", "- Grounded in the sources? (yes/no):",
                  "- Citations point to the right source? (yes/no):"]
    else:
        lines += ["- Said the sources do not contain the answer? (yes/no):",
                  "- Added facts from outside the sources? (yes/no):"]
    lines += ["- Notes:", ""]
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--sample", type=int, default=6, help="questions to sample from the main set")
    parser.add_argument("--seed", type=int, default=0, help="random seed for the sample")
    parser.add_argument("--eval", default="eval/eval_questions.csv")
    parser.add_argument("--out-of-scope", default="eval/out_of_scope_questions.csv")
    parser.add_argument("--out", default="results/answer_check.md")
    parser.add_argument("--chunks", default="data/chunks.jsonl",
                        help="chunks file the index was built from (default: data/chunks.jsonl)")
    add_model_args(parser)
    parser.add_argument("--max-tokens", type=int, default=400,
                        help="cap on each reply's length in tokens (default: 400)")
    parser.add_argument("--delay", type=float, default=0.0,
                        help="seconds to pause between questions (helps with rate limits)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    from .llm import make_generate
    from .retrieve import Retriever

    retriever = Retriever(chunks_path=args.chunks, index_path=args.index, model_name=args.model)
    generate = make_generate(max_tokens=args.max_tokens)
    items = [("in-scope", r) for r in sample_rows(read_rows(args.eval), args.sample, args.seed)]
    items += [("out-of-scope", r) for r in read_rows(args.out_of_scope)]

    entries = []
    for number, (kind, row) in enumerate(items, start=1):
        print(f"[{number}/{len(items)}] {row['question']}")
        reply, hits = run_question(row["question"], retriever, generate)
        info = getattr(generate, "last_info", None)
        entries.append(format_entry(number, kind, row, reply, hits, info))
        if args.delay and number < len(items):
            time.sleep(args.delay)

    header = (
        f"# Answer check, run on {date.today().isoformat()}\n\n"
        f"Top {K} chunks per question. Backend: {describe_backend()}. "
        f"Sample seed: {args.seed}. Replies are capped at {args.max_tokens} tokens, "
        f"so long answers may be cut off. If an answer starts with 'No LLM available', "
        f"the backend was not running and this is only the grounded prompt.\n\n"
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + "\n".join(entries), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
