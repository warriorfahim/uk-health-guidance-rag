import json

from ragdemo.ingest import build_chunks, main


def test_build_chunks_records_source(tmp_path):
    (tmp_path / "page.txt").write_text("word " * 30, encoding="utf-8")
    records = build_chunks(tmp_path, size=10, overlap=2)
    assert records and all(r["source"] == "page.txt" for r in records)


def test_main_writes_chunks_with_given_overlap(tmp_path):
    (tmp_path / "page.txt").write_text(" ".join(f"w{i}" for i in range(30)), encoding="utf-8")
    out = tmp_path / "chunks.jsonl"
    main(raw_dir=str(tmp_path), out_path=str(out), size=10, overlap=0)
    rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 3 and rows[0]["text"].split()[-1] == "w9" and rows[1]["text"].split()[0] == "w10"
