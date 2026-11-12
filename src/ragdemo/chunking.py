"""Split text into overlapping word-based chunks."""


def chunk_text(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Return chunks of about `size` words, each overlapping the previous by `overlap` words."""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must be >= 0 and smaller than size")
    words = text.split()
    if not words:
        return []
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks
