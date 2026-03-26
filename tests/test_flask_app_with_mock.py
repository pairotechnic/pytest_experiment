import pytest
from scripts.flask_app import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    app.config["TESTING"] = True # Enable testing mode
    with app.test_client() as client:
        yield client # Provide the test client instance

def test_get_user(client):
    """Test retrieving a user."""
    # First, add a user
    client.post('/users', json={"id": 2, "name": "Bob"})

    # Then retrieve the user
    response = client.get('/users/2')

    assert response.status_code == 200
    assert response.json == {"id": 2, "name": "Bob"}

def test_get_user_not_found(client):
    """Test retrieving a non-existant user."""
    response = client.get('/users/99')

    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_add_user(client):
    """Test adding a new user."""
    response = client.post('/users', json={"id": 1, "name": "Alice"})

    assert response.status_code == 201
    assert response.json == {"id": 1, "name": "Alice"}

def test_add_duplicate_user(client):
    """Test adding a duplicate user."""
    client.post('/users', json={"id": 3, "name": "Charlie"})
    response = client.post('/users', json={"id": 3, "name": "Charlie"})

    assert response.status_code == 404

@pytest.mark.parametrize("json", [
    {"id": 1, "name": ""},
    {"id": "", "name": "Alice"},
    {"id": 1},
    {"name": "Alice"},
    {},
    {"extra": "abc"},
])
def test_add_user_invalid_request(client, json):
    """Test adding a user with an improper request, missing some mandatory fields"""
    response = client.post('/users', json=json)

    assert response.status_code == 400
    assert response.json == {"error": "Invalid data"}