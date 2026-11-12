from ragdemo.ingest import build_chunks


def test_build_chunks_records_source(tmp_path):
    (tmp_path / "page.txt").write_text("word " * 30, encoding="utf-8")
    records = build_chunks(tmp_path, size=10, overlap=2)
    assert records and all(r["source"] == "page.txt" for r in records)
