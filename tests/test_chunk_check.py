from ragdemo.chunk_check import chunk_hit_rate, first_gold_rank, gold_chunk_ids, normalize

CHUNKS = [
    {"source": "a.txt", "chunk_id": 0, "text": "Intro about the topic.\nPeople aged 30 and under\nare most at risk."},
    {"source": "a.txt", "chunk_id": 1, "text": "Unrelated advice."},
    {"source": "b.txt", "chunk_id": 0, "text": "People aged 30 and under are most at risk."},
]


def test_normalize_collapses_whitespace_and_quotes():
    assert normalize("  It’s  A\nTest ") == "it's a test"


def test_gold_chunk_ids_matches_across_line_breaks_and_source():
    assert gold_chunk_ids(CHUNKS, "a.txt", "people aged 30 and under are most at risk") == [0]
    assert gold_chunk_ids(CHUNKS, "b.txt", "People aged 30") == [0]


def test_gold_chunk_ids_missing_or_empty_phrase():
    assert gold_chunk_ids(CHUNKS, "a.txt", "not in the page") == []
    assert gold_chunk_ids(CHUNKS, "a.txt", "   ") == []


def test_first_gold_rank():
    retrieved = [("b.txt", 0), ("a.txt", 1), ("a.txt", 0)]
    assert first_gold_rank(retrieved, "a.txt", [0]) == 3
    assert first_gold_rank(retrieved, "a.txt", [5]) is None
    assert first_gold_rank([], "a.txt", [0]) is None


def test_chunk_hit_rate():
    ranks = [1, 3, None, 5]
    assert chunk_hit_rate(ranks, 1) == 0.25
    assert chunk_hit_rate(ranks, 3) == 0.5
    assert chunk_hit_rate(ranks, 5) == 0.75
    assert chunk_hit_rate([], 3) == 0.0
