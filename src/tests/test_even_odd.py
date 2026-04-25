```python
import pytest

def even_odd(a):
    if a%2 == 0:
        return "number is even"
    else:
        return "number is odd"

@pytest.mark.parametrize("input, expected", [
    (2, "number is even"),
    (3, "number is odd"),
    (0, "number is even"),
    (-2, "number is even"),
    (-3, "number is odd"),
    (10, "number is even"),
    (11, "number is odd"),
])
def test_even_odd_positive(input, expected):
    assert even_odd(input) == expected

@pytest.mark.parametrize("input, expected", [
    (2.5, "number is even"),  # float
    (3.5, "number is odd"),   # float
    ("2", "number is even"),  # string
    ("3", "number is odd"),   # string
    (None, "number is odd"),  # None
    (True, "number is odd"),  # boolean
    (False, "number is odd"), # boolean
])
def test_even_odd_invalid(input, expected):
    assert even_odd(input) == expected

def test_even_odd_zero_division():
    with pytest.raises(ZeroDivisionError):
        even_odd(0)

def test_even_odd_type_error():
    with pytest.raises(TypeError):
        even_odd("a")
```

Note: The `even_odd` function does not handle invalid inputs correctly. The `test_even_odd_invalid` test case shows that it returns "number is odd" for all invalid inputs. You may want to modify the function to handle these cases correctly.