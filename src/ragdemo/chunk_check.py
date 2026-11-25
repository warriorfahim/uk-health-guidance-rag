"""Chunk-level retrieval check: is the chunk that holds the answer in the top k?

`evaluate` only checks the page (Hit@k). This check needs, for each question, a short phrase copied
word for word from the page that contains the answer, written by hand in
eval/answer_spans.csv (columns: question, expected_source, answer_text). A chunk counts as the
answering chunk if its text contains that phrase, so the same file works for any chunk size.

    python -m ragdemo.chunk_check [--model NAME --index PATH]

Run it against whichever index is currently built (ingest + index first when changing chunking).
Use --model and --index together when the index was built with a different embedding model.
Rows with an empty answer_text are skipped.
"""
import csv
import re


def normalize(text: str) -> str:
    """Lower-case, unify quotes and collapse whitespace so phrases match across line breaks."""
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def gold_chunk_ids(chunks: list[dict], source: str, phrase: str) -> list[int]:
    """chunk_ids of chunks from `source` whose text contains `phrase`."""
    needle = normalize(phrase)
    if not needle:
        return []
    return [
        c["chunk_id"]
        for c in chunks
        if c["source"] == source and needle in normalize(c["text"])
    ]


def first_gold_rank(retrieved: list[tuple[str, int]], source: str, gold_ids: list[int]) -> int | None:
    """1-based rank of the first retrieved (source, chunk_id) that is a gold chunk, else None."""
    gold = set(gold_ids)
    for rank, (src, cid) in enumerate(retrieved, start=1):
        if src == source and cid in gold:
            return rank
    return None


def chunk_hit_rate(ranks: list[int | None], k: int) -> float:
    """Share of questions whose answering chunk is in the top k."""
    if not ranks:
        return 0.0
    return sum(1 for r in ranks if r is not None and r <= k) / len(ranks)


def read_spans(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(spans_path: str = "eval/answer_spans.csv", ks=(1, 3, 5),
         model_name: str | None = None, index_path: str = "data/index.faiss",
         query_prefix: str = "", chunks_path: str = "data/chunks.jsonl",
         mode: str = "dense") -> None:
    rows = read_spans(spans_path)
    filled = [r for r in rows if (r.get("answer_text") or "").strip()]
    print(f"{len(filled)} of {len(rows)} questions have an answer_text in {spans_path}")
    if not filled:
        print("Nothing to check. Add a short verbatim phrase from the answering sentence to answer_text.")
        return

    from .index import DEFAULT_MODEL
    from .retrieve import Retriever

    model_name = model_name or DEFAULT_MODEL
    print(f"Model: {model_name}, chunks: {chunks_path}, index: {index_path}")
    if mode != "dense":
        print(f"Search mode: {mode}")
    if query_prefix:
        print(f"Query prefix: {query_prefix!r}")
    retriever = Retriever(chunks_path=chunks_path, index_path=index_path, model_name=model_name,
                          query_prefix=query_prefix, mode=mode)
    ranks, not_found, details = [], [], []
    for row in filled:
        question, source, phrase = row["question"], row["expected_source"], row["answer_text"]
        gold = gold_chunk_ids(retriever.chunks, source, phrase)
        if not gold:
            not_found.append((question, source, phrase))
            continue
        hits = retriever.search(question, k=max(ks))
        retrieved = [(h["source"], h["chunk_id"]) for h in hits]
        rank = first_gold_rank(retrieved, source, gold)
        ranks.append(rank)
        details.append((question, source, gold, retrieved, rank))

    print(f"Checked {len(ranks)} questions; answer phrase not found in any chunk for {len(not_found)}")
    for k in ks:
        print(f"Chunk-Hit@{k}: {chunk_hit_rate(ranks, k):.2f}")
    kmax = max(ks)
    missed = [d for d in details if d[4] is None]
    print(f"\nAnswering chunk not in the top {kmax}: {len(missed)} of {len(ranks)}")
    for question, source, gold, retrieved, _ in missed:
        got = ", ".join(f"{s}#{c}" for s, c in retrieved)
        print(f"- {question}\n    answering chunk(s): {source}#{', #'.join(str(g) for g in gold)}\n    got: {got}")
    if not_found:
        print(f"\nPhrase not found in any chunk of the expected page ({len(not_found)}):")
        print("(check the spelling, or the phrase may straddle a chunk boundary: use a shorter phrase)")
        for question, source, phrase in not_found:
            print(f"- {question}\n    {source}: {phrase!r}")


if __name__ == "__main__":
    import argparse

    from .index import add_model_args

    parser = argparse.ArgumentParser(description="Chunk-level hit rate (is the answering chunk in the top k?).")
    add_model_args(parser, query_prefix=True, mode=True)
    args = parser.parse_args()
    main(model_name=args.model, index_path=args.index, query_prefix=args.query_prefix,
         chunks_path=args.chunks, mode=args.mode)
