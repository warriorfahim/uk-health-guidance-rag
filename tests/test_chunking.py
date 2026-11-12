import pytest

from ragdemo.chunking import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []


def test_short_text_is_one_chunk():
    assert chunk_text("one two three", size=10, overlap=2) == ["one two three"]


def test_chunks_overlap():
    text = " ".join(str(i) for i in range(20))
    chunks = chunk_text(text, size=10, overlap=4)
    assert chunks[0].split()[-4:] == chunks[1].split()[:4]


def test_all_words_are_covered():
    words = [str(i) for i in range(53)]
    chunks = chunk_text(" ".join(words), size=10, overlap=3)
    covered = {w for c in chunks for w in c.split()}
    assert covered == set(words)


def test_bad_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text("a b c", size=5, overlap=5)
