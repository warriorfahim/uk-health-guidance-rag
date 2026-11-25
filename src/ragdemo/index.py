"""Embed chunks and build a FAISS index (heavy imports are inside functions)."""
import json

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"  # was all-MiniLM-L6-v2 until 2026-11-23; see docs/evaluation.md


# bge's recommended instruction for short search queries; documents are indexed without it.
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def add_model_args(parser, query_prefix: bool = False, mode: bool = False) -> None:
    """Add --model, --chunks and --index options (shared by index, evaluate, chunk_check and answer_check).

    With `query_prefix=True` also add --query-prefix, text put in front of each question before it
    is embedded (the index itself is not changed, so it needs no rebuild). With `mode=True` also add
    --mode (dense, bm25 or hybrid), how chunks are searched.
    """
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"embedding model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--chunks", default="data/chunks.jsonl",
                        help="chunks file to embed or search (default: data/chunks.jsonl)")
    parser.add_argument("--index", default="data/index.faiss",
                        help="FAISS index file to write or read (default: data/index.faiss)")
    if mode:
        parser.add_argument("--mode", choices=("dense", "bm25", "hybrid"), default="dense",
                            help="how to search: dense (default), bm25 keywords only, or hybrid of both")
    if query_prefix:
        parser.add_argument("--query-prefix", default="",
                            help="text put before each question when searching (default: none; "
                                 f"bge suggests {BGE_QUERY_PREFIX!r})")


def load_chunks(path: str = "data/chunks.jsonl") -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def embed(texts: list[str], model_name: str = DEFAULT_MODEL):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True).astype("float32")


def main(chunks_path: str = "data/chunks.jsonl", index_path: str = "data/index.faiss",
         model_name: str = DEFAULT_MODEL) -> None:
    import faiss
    chunks = load_chunks(chunks_path)
    vectors = embed([c["text"] for c in chunks], model_name)
    index = faiss.IndexFlatIP(vectors.shape[1])  # cosine similarity on normalised vectors
    index.add(vectors)
    faiss.write_index(index, index_path)
    print(f"Indexed {len(chunks)} chunks with {model_name}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Embed data/chunks.jsonl and build a FAISS index.")
    add_model_args(parser)
    args = parser.parse_args()
    main(chunks_path=args.chunks, index_path=args.index, model_name=args.model)
