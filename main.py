import requests
import datetime as dt
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

ORIGIN_CITY = "Toronto"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

prices_data = data_manager.get_prices_rows()
users_data = data_manager.get_users_rows()

origin_city_iata_code = flight_search.get_destination_code(ORIGIN_CITY)
from_time = dt.datetime.today().date() + dt.timedelta(12)

for city_data in prices_data:
    row_id = city_data["id"]
    destination_city = city_data["city"]

    if len(city_data["iataCode"]) == 0:
        city_data["iataCode"] = flight_search.get_destination_code(destination_city)

    destination_city_iata_code = city_data["iataCode"]
    minimum_number_of_days = city_data["minimumNumberOfDays"]
    length_of_trip = city_data["lengthOfTrip"]
    cheapest_round_trip_price = city_data["lowestPrice"]
    departing_date = city_data["departingDate"]
    arrival_date = city_data["arrivalDate"]

    departing_flight_data = FlightData()

    cheapest_departing_flight = flight_search.search_for_cheapest_flight(
        origin_city=origin_city_iata_code,
        destination_city=destination_city_iata_code,
        from_time=from_time,
        to_time=(from_time + dt.timedelta(12))
    )

    departing_flight_data.retrieve_and_print_info(cheapest_departing_flight)

    return_flight_data = FlightData()

    returning_date_start = (dt.datetime.strptime(departing_flight_data.arrival_date, "%Y-%m-%d") + dt.timedelta(minimum_number_of_days)).date()
    returning_date_end = returning_date_start + dt.timedelta(length_of_trip - minimum_number_of_days)

    cheapest_return_flight = flight_search.search_for_cheapest_flight(
        origin_city=destination_city_iata_code,
        destination_city=origin_city_iata_code,
        from_time=returning_date_start,
        to_time=returning_date_end
    )

    return_flight_data.retrieve_and_print_info(cheapest_return_flight)

    total_price = departing_flight_data.price + return_flight_data.price

    if total_price < cheapest_round_trip_price:
        city_data["lowestPrice"] = total_price
        city_data["departingDate"] = departing_flight_data.departing_date
        city_data["arrivalDate"] = return_flight_data.arrival_date

        notification_manager.send_message(
            price=total_price,
            origin=origin_city_iata_code,
            destination=destination_city_iata_code,
            departure_date=departing_flight_data.departing_date,
            return_date=return_flight_data.arrival_date
        )

        for user_data in users_data:
            user_name = user_data["whatIsYourFirstName?"]
            user_email = user_data["enterYourEmailAddress"]

            notification_manager.send_email(receiver_email=user_email, receiver_name=user_name, departing_flight_data=departing_flight_data, return_flight_data=return_flight_data)

    data_manager.update_prices_row(row_id, city_data)

    print()
