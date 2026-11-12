"""Read .txt pages from data/raw and write overlapping chunks to data/chunks.jsonl."""
import json
import sys
from pathlib import Path

from .chunking import chunk_text


def build_chunks(raw_dir: Path, size: int = 200, overlap: int = 40) -> list[dict]:
    records = []
    for path in sorted(raw_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text, size, overlap)):
            records.append({"source": path.name, "chunk_id": i, "text": chunk})
    return records


def main(raw_dir: str = "data/raw", out_path: str = "data/chunks.jsonl",
         size: int = 200, overlap: int = 40) -> None:
    records = build_chunks(Path(raw_dir), size, overlap)
    if not records:
        sys.exit(f"No .txt files found in {raw_dir}. Add cleaned pages first.")
    with open(out_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} chunks from {raw_dir} to {out_path}")


if __name__ == "__main__":
    main()
