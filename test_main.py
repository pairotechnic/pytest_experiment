
from main import get_weather, add, divide
import pytest

def test_get_weather():
    assert get_weather(15) == "cold"
    assert get_weather(25) == "hot"

def test_add():
    assert add(2, 3) == 5, "2 + 3 should be 5"
    assert add(-1, 1) == 0, "-1 + 1 should be 0"
    assert add(0, 0) == 0, "0 + 0 should be 0"

def test_divide():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)