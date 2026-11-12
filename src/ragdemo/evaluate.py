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


def main(eval_path: str = "eval/eval_questions.csv", ks=(1, 3, 5)) -> None:
    from .retrieve import Retriever
    retriever = Retriever()
    questions, expected = [], []
    with open(eval_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            questions.append(row["question"])
            expected.append(row["expected_source"])
    ranked = [[h["source"] for h in retriever.search(q, k=max(ks))] for q in questions]
    for k in ks:
        print(f"Hit@{k}: {hit_rate_at_k(ranked, expected, k):.2f}")


if __name__ == "__main__":
    main()
