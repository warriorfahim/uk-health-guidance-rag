import pytest

from ragdemo.evaluate import hit_rate_at_k


def test_hit_rate_at_k():
    ranked = [["a", "b", "c"], ["x", "y", "z"], ["m", "n", "o"]]
    expected = ["a", "z", "q"]
    assert hit_rate_at_k(ranked, expected, k=1) == pytest.approx(1 / 3)
    assert hit_rate_at_k(ranked, expected, k=3) == pytest.approx(2 / 3)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        hit_rate_at_k([["a"]], ["a", "b"], k=1)


def test_find_misses_lists_only_unretrieved():
    from ragdemo.evaluate import find_misses

    ranked = [["a", "b"], ["c", "d"]]
    out = find_misses(["q1", "q2"], ranked, ["b", "a"], k=2)
    assert out == [("q2", "a", ["c", "d"])]
    assert find_misses(["q1"], [["a", "b"]], ["b"], k=1) == [("q1", "b", ["a"])]
