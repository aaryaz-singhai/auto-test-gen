# tests/test_sample.py
import pytest
from sample import subtraction

def test_subtraction_valid_inputs():
    assert subtraction(5, 3) == 2
    assert subtraction(-5, 3) == -8
    assert subtraction(0, 0) == 0
    assert subtraction(-5, -3) == -2

def test_subtraction_invalid_inputs():
    with pytest.raises(TypeError):
        subtraction('a', 3)
    with pytest.raises(TypeError):
        subtraction(3, 'b')
    with pytest.raises(TypeError):
        subtraction('a', 'b')

def test_subtraction_non_numeric_inputs():
    with pytest.raises(TypeError):
        subtraction(3, [1, 2, 3])
    with pytest.raises(TypeError):
        subtraction({1: 2}, 3)

def test_subtraction_negative_numbers():
    assert subtraction(-5, 3) == -8
    assert subtraction(-5, -3) == -2

def test_subtraction_large_numbers():
    assert subtraction(1000000, 3) == 999997
    assert subtraction(-1000000, 3) == -1000003

def test_subtraction_zero():
    assert subtraction(0, 3) == -3
    assert subtraction(3, 0) == 3
    assert subtraction(0, 0) == 0