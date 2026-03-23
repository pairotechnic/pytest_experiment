
from main import get_weather, add, divide, UserManager
import pytest

@pytest.fixture
def user_manager():
    """Creates a fresh instance of UserManager before each test, and cleans up afterwards"""
    user_manager = UserManager()
    yield user_manager # Provide the fixture instance
    user_manager.users.clear() # Cleanup step not needed for in-memory, but useful for real DBs

def test_add_user(user_manager):
    assert user_manager.add_user("john_doe", "john@example.com") == True
    assert user_manager.get_user("john_doe") == "john@example.com"

def test_add_duplicate_user(user_manager):
    user_manager.add_user("john_doe", "john@example.com")
    with pytest.raises(ValueError, match="User already exists"):
        user_manager.add_user("john_doe", "another@example.com")
    assert user_manager.get_user("john_doe") == "john@example.com"

def test_get_nonexistant_user(user_manager):
    assert user_manager.get_user("john_doe") == None

def test_get_existing_user(user_manager):
    assert user_manager.add_user("john_doe", "john@example.com") == True
    assert user_manager.get_user("john_doe") == "john@example.com"

def test_delete_non_existant_user(user_manager):
    assert user_manager.delete_user("john_doe") == None
    assert user_manager.get_user("john_doe") == None

def test_delete_existing_user(user_manager):
    assert user_manager.add_user("john_doe", "john@example.com") == True
    assert user_manager.get_user("john_doe") == "john@example.com"
    assert user_manager.delete_user("john_doe") == None
    assert user_manager.get_user("john_doe") == None

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