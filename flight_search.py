import os
import time
import requests
import datetime as dt
from pprint import pprint

# This class is responsible for talking to the Flight Search API.
class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self.AMADEUS_ENDPOINT = "https://test.api.amadeus.com"
        self.TOKEN_ENDPOINT = f"{self.AMADEUS_ENDPOINT}/v1/security/oauth2/token"
        self.CITY_SEARCH_ENDPOINT = f"{self.AMADEUS_ENDPOINT}/v1/reference-data/locations/cities"
        self._token = self._get_new_token()


    def _get_new_token(self):
        """Generates a new access token"""
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }

        response = requests.post(url=self.TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()["access_token"]


    def get_destination_code(self, city_name):
        """Returns the IATA code for the specified city name"""
        header = {
            "Authorization": f"Bearer {self._token}"
        }

        body = {
            "keyword": city_name
        }
        response = requests.get(url=self.CITY_SEARCH_ENDPOINT, headers=header, params=body)
        return response.json()["data"][0]["iataCode"]


    def search_for_cheapest_flight(self, origin_city, destination_city, from_time, to_time):
        """Returns the details of the cheapest flight found, departing within the next 6 months"""
        header = {
            "Authorization": f"Bearer {self._token}"
        }

        min_price = 9999.99
        cheapest_flight = {}
        dictionaries = {}

        # while from_time != to_time:
        query = {
            "originLocationCode": origin_city,
            "destinationLocationCode": destination_city,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "travelClass": "ECONOMY",
            "currencyCode": "CAD"
        }

        response = requests.get(url=f"{self.AMADEUS_ENDPOINT}/v2/shopping/flight-offers",
                     headers=header, params=query)
        try:
            data = response.json()["data"]
        except KeyError:
            data = []
            pprint(response.json())

        try:
            dictionary = response.json()["dictionaries"]
        except KeyError:
            dictionary = {
                'aircraft': {},
                 'carriers': {},
                 'currencies': {},
                 'locations': {}}

        for flight_data in data:
            flight_total_price = float(flight_data["price"]["total"])
            if min_price > flight_total_price:
                min_price = flight_total_price
                cheapest_flight = flight_data
                dictionaries = dictionary
        from_time += dt.timedelta(1)
        time.sleep(0.5)

        return {"cheapest_flight": cheapest_flight,
            "info_dictionary": dictionaries}
