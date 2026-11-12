"""Embed chunks and build a FAISS index (heavy imports are inside functions)."""
import json

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


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
    main()
