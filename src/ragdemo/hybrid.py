"""Keyword (BM25) scoring and rank fusion for hybrid search. Standard library only.

The settings below are the ones fixed in docs/evaluation.md ("Hybrid search: decision rule")
before any run, and are not tuned.
"""
import math
import re
from collections import Counter

K1 = 1.5  # BM25 term-frequency saturation
B = 0.75  # BM25 length normalisation
POOL = 20  # chunks taken from each ranking before fusion
RRF_K = 60  # reciprocal rank fusion constant


def tokenize(text: str) -> list[str]:
    """Lower-case word tokens (letters, digits, underscore); no stop words or stemming."""
    return re.findall(r"\w+", text.lower())


class BM25:
    """Okapi BM25 over a list of documents. Each distinct query word counts once."""

    def __init__(self, docs: list[str], k1: float = K1, b: float = B):
        self.k1, self.b = k1, b
        self.term_counts = [Counter(tokenize(d)) for d in docs]
        self.lengths = [sum(c.values()) for c in self.term_counts]
        n = len(docs)
        self.avg_length = sum(self.lengths) / n if n else 0.0
        doc_freq: Counter = Counter()
        for counts in self.term_counts:
            doc_freq.update(counts.keys())
        self.idf = {t: math.log(1 + (n - df + 0.5) / (df + 0.5)) for t, df in doc_freq.items()}

    def scores(self, query: str) -> list[float]:
        """BM25 score of every document for the query (0.0 where no query word occurs)."""
        terms = [t for t in set(tokenize(query)) if t in self.idf]
        out = []
        for counts, length in zip(self.term_counts, self.lengths):
            norm = 1 - self.b + self.b * length / self.avg_length if self.avg_length else 1.0
            score = 0.0
            for t in terms:
                f = counts.get(t, 0)
                if f:
                    score += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * norm)
            out.append(score)
        return out

    def top(self, query: str, k: int) -> list[int]:
        """Indexes of the k best-scoring documents, best first; documents scoring 0 are left out."""
        scores = self.scores(query)
        ranked = sorted((i for i, s in enumerate(scores) if s > 0), key=lambda i: (-scores[i], i))
        return ranked[:k]


def rrf(rankings: list[list[int]], k: int = RRF_K) -> list[tuple[int, float]]:
    """Reciprocal rank fusion: (id, score) best first, score = sum of 1 / (k + rank) over the lists."""
    fused: dict[int, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return sorted(fused.items(), key=lambda pair: (-pair[1], pair[0]))
