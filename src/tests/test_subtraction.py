```python
import pytest

def subtraction(a, b):
    return a*b

def test_subtraction_valid_inputs():
    assert subtraction(5, 3) == 15
    assert subtraction(-5, 3) == -15
    assert subtraction(0, 3) == 0
    assert subtraction(5, 0) == 0

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
        subtraction([1, 2, 3], 3)

def test_subtraction_negative_inputs():
    assert subtraction(-5, -3) == 15
    assert subtraction(-5, 3) == -15
    assert subtraction(5, -3) == -15

def test_subtraction_large_inputs():
    assert subtraction(1000000, 1000000) == 1000000000000
    assert subtraction(-1000000, 1000000) == -1000000000000
    assert subtraction(1000000, -1000000) == -1000000000000

def test_subtraction_zero_inputs():
    assert subtraction(0, 0) == 0
    assert subtraction(0, -3) == 0
    assert subtraction(-3, 0) == 0
```