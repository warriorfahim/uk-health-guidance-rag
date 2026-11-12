"""Semantic search over the FAISS index."""
from .index import DEFAULT_MODEL, load_chunks


class Retriever:
    def __init__(self, chunks_path: str = "data/chunks.jsonl", index_path: str = "data/index.faiss",
                 model_name: str = DEFAULT_MODEL):
        import faiss
        from sentence_transformers import SentenceTransformer
        self.chunks = load_chunks(chunks_path)
        self.index = faiss.read_index(index_path)
        self.model = SentenceTransformer(model_name)

    def search(self, query: str, k: int = 5) -> list[dict]:
        vec = self.model.encode([query], normalize_embeddings=True).astype("float32")
        scores, ids = self.index.search(vec, k)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            hit = dict(self.chunks[idx])
            hit["score"] = float(score)
            results.append(hit)
        return results
