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
