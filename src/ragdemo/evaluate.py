"""Retrieval evaluation: hit rate at k on a hand-written question set."""
import csv


def hit_rate_at_k(ranked_sources: list[list[str]], expected: list[str], k: int) -> float:
    """Share of questions whose expected source appears in the top-k retrieved sources."""
    if len(ranked_sources) != len(expected):
        raise ValueError("ranked_sources and expected must have the same length")
    if not expected:
        return 0.0
    hits = sum(1 for ranked, exp in zip(ranked_sources, expected) if exp in ranked[:k])
    return hits / len(expected)


def find_misses(
    questions: list[str], ranked_sources: list[list[str]], expected: list[str], k: int
) -> list[tuple[str, str, list[str]]]:
    """Questions whose expected source is not in the top-k: (question, expected, top-k sources)."""
    return [
        (q, exp, ranked[:k])
        for q, ranked, exp in zip(questions, ranked_sources, expected)
        if exp not in ranked[:k]
    ]


def parse_args(argv: list[str] | None = None):
    import argparse

    from .index import add_model_args

    parser = argparse.ArgumentParser(description="Hit@k on the retrieval eval set.")
    parser.add_argument("--misses", action="store_true",
                        help="also list questions whose source was not in the top 5")
    add_model_args(parser, query_prefix=True)
    return parser.parse_args(argv)


def main(
    eval_path: str = "eval/eval_questions.csv", ks=(1, 3, 5), show_misses: bool = False,
    model_name: str | None = None, index_path: str = "data/index.faiss", query_prefix: str = "",
    chunks_path: str = "data/chunks.jsonl",
) -> None:
    from .index import DEFAULT_MODEL
    from .retrieve import Retriever
    model_name = model_name or DEFAULT_MODEL
    print(f"Model: {model_name}, chunks: {chunks_path}, index: {index_path}")
    if query_prefix:
        print(f"Query prefix: {query_prefix!r}")
    retriever = Retriever(chunks_path=chunks_path, index_path=index_path, model_name=model_name,
                          query_prefix=query_prefix)
    questions, expected = [], []
    with open(eval_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            questions.append(row["question"])
            expected.append(row["expected_source"])
    ranked = [[h["source"] for h in retriever.search(q, k=max(ks))] for q in questions]
    for k in ks:
        print(f"Hit@{k}: {hit_rate_at_k(ranked, expected, k):.2f}")
    if show_misses:
        kmax = max(ks)
        misses = find_misses(questions, ranked, expected, kmax)
        print(f"\nMissed at k={kmax}: {len(misses)} of {len(questions)}")
        for q, exp, got in misses:
            print(f"- {q}\n    expected: {exp}\n    got:      {', '.join(got)}")


if __name__ == "__main__":
    args = parse_args()
    main(show_misses=args.misses, model_name=args.model, index_path=args.index,
         query_prefix=args.query_prefix, chunks_path=args.chunks)
