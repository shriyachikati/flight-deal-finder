import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.prices_endpoint = os.getenv("SHEETY_PRICES_ENDPOINT")
        self.authorization = os.getenv("AUTHORIZATION")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.authorization
        }

        self.users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")

    def get_prices_rows(self):
        """Retrieves all the rows present in the Google sheet for prices"""
        response = requests.get(url=self.prices_endpoint, headers=self.headers)
        return response.json()["prices"]

    def update_prices_row(self, index, row):
        """Updates the data in the specified row in the Google sheet for prices"""
        body = {
            "price" : row
        }
        response = requests.put(url=f"{self.prices_endpoint}/{index}", json=body, headers=self.headers)

    def get_users_rows(self):
        """Retrieves all the rows present in the Google sheet for users"""
        response = requests.get(url=self.users_endpoint, headers=self.headers)
        return response.json()["users"]