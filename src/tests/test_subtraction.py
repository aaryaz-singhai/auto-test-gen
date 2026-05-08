# tests/test_subtraction.py
from sample import subtraction
import pytest

def test_subtraction_valid():
    assert subtraction(5, 3) == 2
    assert subtraction(-5, 3) == -8
    assert subtraction(0, 0) == 0
    assert subtraction(-5, -3) == -2

def test_subtraction_invalid_type():
    with pytest.raises(TypeError):
        subtraction("a", 3)
    with pytest.raises(TypeError):
        subtraction(3, "b")

def test_subtraction_invalid_input():
    with pytest.raises(ValueError):
        subtraction(5, "a")
    with pytest.raises(ValueError):
        subtraction("a", 3)
    with pytest.raises(ValueError):
        subtraction("a", "b")

def test_subtraction_edge_cases():
    assert subtraction(5, 0) == 5
    assert subtraction(-5, 0) == -5
    assert subtraction(0, 5) == -5
    assert subtraction(0, -5) == 5