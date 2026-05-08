from sample import multiple_of_ten
import pytest

def test_multiple_of_ten_integer():
    assert multiple_of_ten(10) == "divisible by 10"
    assert multiple_of_ten(20) == "divisible by 10"
    assert multiple_of_ten(30) == "divisible by 10"

def test_multiple_of_ten_non_multiple_of_ten():
    assert multiple_of_ten(1) is None
    assert multiple_of_ten(2) is None
    assert multiple_of_ten(3) is None

def test_multiple_of_ten_non_integer():
    with pytest.raises(TypeError):
        multiple_of_ten("a")

def test_multiple_of_ten_non_numeric():
    with pytest.raises(TypeError):
        multiple_of_ten("a")
    with pytest.raises(TypeError):
        multiple_of_ten(None)

def test_multiple_of_ten_empty_string():
    with pytest.raises(TypeError):
        multiple_of_ten("")

def test_multiple_of_ten_zero():
    assert multiple_of_ten(0) is None