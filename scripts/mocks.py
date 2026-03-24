import requests
from requests import get
# import sqlite3
from sqlite3 import connect

# For testing Mock API request
def get_weather(city):
    # response = requests.get(f"https://api.weather.com/v1/{city}")
    response = get(f"https://api.weather.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else :
        raise ValueError("Could not fetch weather data")
    
# For testing Mock DB connection and cursor
def save_user(name, age):
    # conn = sqlite3.connect("users.db")
    conn = connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

class APIClient:
    """Simulates an external API Client."""
    def get_user_data(self, user_id):
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        raise ValueError("API request failed")
    
class UserService:
    """Uses APIClient data to fetch user data and process it."""
    def __init__(self, api_client):
        self.api_client = api_client # Dependency injection

    def get_username(self, user_id):
        """Fetches a user and returns their username in uppercase."""
        user_data = self.api_client.get_user_data(user_id) # Calls API Client
        return user_data["name"].upper() # Process the output