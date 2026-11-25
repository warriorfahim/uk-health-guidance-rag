import pytest

from ragdemo.hybrid import BM25, rrf, tokenize
from ragdemo.retrieve import MODES, Retriever


def test_tokenize_lowercases_and_splits_on_non_word_characters():
    assert tokenize("Below 2 C, e.g. Hello-World!") == ["below", "2", "c", "e", "g", "hello", "world"]


DOCS = [
    "measles vaccine schedule for children",
    "prolonged periods below 2 degrees put people at risk in cold weather",
    "the weather was cold",
    "unrelated text about mosquitoes",
]


def test_bm25_ranks_the_matching_document_first():
    bm25 = BM25(DOCS)
    assert bm25.top("cold weather risk", k=3)[0] == 1


def test_bm25_rare_word_beats_common_word():
    bm25 = BM25(["apple banana", "apple cherry", "apple banana cherry date"])
    # "date" occurs in one document only, "apple" in all of them
    assert bm25.top("apple date", k=1) == [2]


def test_bm25_leaves_out_documents_with_no_matching_word():
    bm25 = BM25(DOCS)
    assert bm25.top("mosquitoes", k=5) == [3]
    assert bm25.top("zzzz", k=5) == []
    assert bm25.top("", k=5) == []


def test_bm25_empty_corpus():
    assert BM25([]).top("anything", k=3) == []


def test_bm25_counts_each_query_word_once():
    bm25 = BM25(DOCS)
    assert bm25.scores("cold") == pytest.approx(bm25.scores("cold cold cold"))


def test_rrf_rewards_chunks_in_both_lists_and_orders_by_score():
    fused = rrf([[10, 20, 30], [20, 40]])
    ids = [i for i, _ in fused]
    assert ids[0] == 20 and set(ids) == {10, 20, 30, 40}
    scores = dict(fused)
    assert scores[20] == pytest.approx(1 / 62 + 1 / 61)
    assert scores[10] == pytest.approx(1 / 61)


def test_rrf_ties_go_to_the_lower_id_and_empty_input_is_empty():
    assert [i for i, _ in rrf([[5], [3]])] == [3, 5]
    assert rrf([]) == [] and rrf([[], []]) == []


def test_retriever_rejects_unknown_mode_without_loading_anything():
    assert MODES == ("dense", "bm25", "hybrid")
    with pytest.raises(ValueError):
        Retriever(mode="fuzzy")
