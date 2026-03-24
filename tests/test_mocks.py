'''
    mocker.patch needs a string as parameter, with at least 1 dot

    This is what mocker.patch does internally : 
    target, attribute = target.rsplit('.', 1)

    It requires a dot in the string because it always splits into two parts — the object to look up, 
    and the attribute on that object to replace. 
    "connect" has no dot, so it can't be split, and it fails immediately.

    This is why, this fails : 
    mock_get = mocker.patch("get")

    But this works : 
    mock_get = mocker.patch("scripts.mocks.get")

    If I did :
    import requests
    requests.get(), 
    then requests lives in the scripts.mocks namespace
    And, I need to do 
    mock_get = mocker.patch("scripts.mocks.requests.get")
    This will work, but not explicit, and not preferred : 
    mock_get = mocker.patch("requests.get")
    
    If I did :
    from requests import get
    get(), 
    then get lives in the scripts.mocks namespace
    And I need to do 
    mock_get = mocker.patch("scripts.mocks.get")
    
    This will not work, because Patching "requests.get" would replace it in the requests module, 
    but scripts.mocks already has its own reference to the original — 
    so your patch never intercepts it.
    mock_get = mocker.patch("requests.get") 


'''

import pytest
from scripts.mocks import get_weather, save_user, UserService, APIClient

def test_get_weather_success(mocker):
    # Mock requests.get

    # Use when response = requests.get(f"https://api.weather.com/v1/{city}")
    # mock_get = mocker.patch("requests.get")
    # mock_get = mocker.patch("scripts.mocks.requests.get")

    # Use when response = get(f"https://api.weather.com/v1/{city}")
    mock_get = mocker.patch("scripts.mocks.get")
    # mock_get = mocker.patch("get") # Incorrect

    # Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}

    # Call function
    result = get_weather("Dubai")

    # Assertions
    assert result == {"temperature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")

def test_get_weather_failure(mocker):
    # Mock requests.get
    # mock_get = mocker.patch("scripts.mocks.requests.get")
    mock_get = mocker.patch("scripts.mocks.get")

    # Set return values
    mock_get.return_value.status_code = 404

    with pytest.raises(ValueError, match="Could not fetch weather data"):
        get_weather("Dholakpur")

def test_save_user(mocker):
    # mock_conn = mocker.patch("sqlite3.connect")
    # mock_conn = mocker.patch("scripts.mocks.sqlite3.connect")

    mock_conn = mocker.patch("scripts.mocks.connect")
    # mock_conn = mocker.patch("connect") # Incorrect 

    mock_cursor = mock_conn.return_value.cursor.return_value

    save_user("Alice", 30)

    mock_conn.assert_called_once_with("users.db")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30)
    )
    mock_conn.return_value.commit.assert_called_once()
    mock_conn.return_value.close.assert_called_once()

def test_get_username(mocker):
    mock_api_client = mocker.Mock(spec=APIClient) # Create a mock APIClient object

    # Mock get_user_data to return a fake user
    mock_api_client.get_user_data.return_value = {"id": 1, "name": "Alice"}

    service = UserService(mock_api_client) # Inject mock APIClient object

    result = service.get_username(1) # Call real method that depends on the mock object

    # Assertions
    assert result == "ALICE" # Check if processing was done correctly
    mock_api_client.get_user_data.assert_called_once_with(1) # Ensure correct API called

