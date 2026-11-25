"""Search over the FAISS index: dense (default), keyword (BM25) or hybrid of the two."""
from .hybrid import BM25, POOL, rrf
from .index import DEFAULT_MODEL, load_chunks

MODES = ("dense", "bm25", "hybrid")


class Retriever:
    def __init__(self, chunks_path: str = "data/chunks.jsonl", index_path: str = "data/index.faiss",
                 model_name: str = DEFAULT_MODEL, query_prefix: str = "", mode: str = "dense"):
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, not {mode!r}")
        import faiss
        from sentence_transformers import SentenceTransformer
        self.chunks = load_chunks(chunks_path)
        self.index = faiss.read_index(index_path)
        self.model = SentenceTransformer(model_name)
        self.query_prefix = query_prefix
        self.mode = mode
        self.bm25 = BM25([c["text"] for c in self.chunks]) if mode != "dense" else None

    def _dense(self, query: str, k: int) -> list[tuple[int, float]]:
        """(chunk row, cosine score) for the k nearest chunks, best first."""
        vec = self.model.encode([self.query_prefix + query], normalize_embeddings=True).astype("float32")
        scores, ids = self.index.search(vec, k)
        return [(int(idx), float(score)) for score, idx in zip(scores[0], ids[0]) if idx != -1]

    def search(self, query: str, k: int = 5) -> list[dict]:
        """Top k chunks with a "score": cosine for dense, BM25 for bm25, fused rank score for hybrid."""
        if self.mode == "dense":
            pairs = self._dense(query, k)
        elif self.mode == "bm25":
            scores = self.bm25.scores(query)
            pairs = [(i, scores[i]) for i in self.bm25.top(query, k)]
        else:
            dense_ids = [i for i, _ in self._dense(query, POOL)]
            pairs = rrf([dense_ids, self.bm25.top(query, POOL)])[:k]
        results = []
        for idx, score in pairs:
            hit = dict(self.chunks[idx])
            hit["score"] = score
            results.append(hit)
        return results
