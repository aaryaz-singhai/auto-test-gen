# tests/test_even_odd.py
import pytest
from sample import even_odd

def test_even():
    assert even_odd(4) == "number is even"

def test_odd():
    assert even_odd(3) == "number is odd"

def test_zero():
    assert even_odd(0) == "number is even"

def test_negative_even():
    assert even_odd(-4) == "number is even"

def test_negative_odd():
    assert even_odd(-3) == "number is odd"

def test_non_integer():
    with pytest.raises(TypeError):
        even_odd("a")

def test_non_numeric():
    with pytest.raises(TypeError):
        even_odd([1, 2, 3])

def test_invalid_input():
    with pytest.raises(TypeError):
        even_odd(None)

def test_integer_string():
    with pytest.raises(TypeError):
        even_odd("123")

def test_float():
    assert even_odd(3.5) == "number is odd"

def test_list_of_integers():
    with pytest.raises(TypeError):
        even_odd([1, 2, 3])