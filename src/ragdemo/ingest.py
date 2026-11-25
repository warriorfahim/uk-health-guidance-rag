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
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    print(f"Wrote {len(records)} chunks from {raw_dir} to {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split pages into overlapping word chunks.")
    parser.add_argument("--raw", default="data/raw", help="folder of .txt pages")
    parser.add_argument("--out", default="data/chunks.jsonl", help="chunks file to write")
    parser.add_argument("--size", type=int, default=200, help="words per chunk")
    parser.add_argument("--overlap", type=int, default=40, help="words shared with the previous chunk")
    args = parser.parse_args()
    main(raw_dir=args.raw, out_path=args.out, size=args.size, overlap=args.overlap)
