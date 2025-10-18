class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = None
        self.departure_airport_code = ""
        self.arrival_airport_code = ""

        self.departing_terminal = ""
        self.arrival_terminal = ""

        self.departing_time = ""
        self.arrival_time = ""
        self.departing_date = ""
        self.arrival_date = ""

        self.duration = ""

        self.flight_durations = []
        self.layovers = []
        self.carriers = []
        self.aircraft = []

    def get_duration(self, duration_string):
        return duration_string[2:]

    def retrieve_and_print_info(self, flight_data):
        """Retrieves the flight data and prints it to the console"""
        flight_dictionary = flight_data["info_dictionary"]
        flight_details = flight_data["cheapest_flight"]

        self.price = float(flight_details["price"]["total"])
        self.duration = self.get_duration(flight_details["itineraries"][0]["duration"])

        flight_itineraries = flight_details["itineraries"][0]["segments"]

        for journey_leg in flight_itineraries:
            # Aircraft in the itineraries
            try:
                self.aircraft.append(flight_dictionary["aircraft"][journey_leg["aircraft"]["code"]])
            except KeyError:
                self.aircraft.append("N/A")

            # Carriers of flights in itineraries
            try:
                self.carriers.append(flight_dictionary["carriers"][journey_leg["operating"]["carrierCode"]])
            except KeyError:
                self.carriers.append("N/A")

            # Layovers in the journey
            try:
                self.layovers.append(journey_leg["arrival"]["iataCode"])
            except KeyError:
                self.layovers.append("N/A")

            # Durations of each trip in the itinerary
            try:
                self.flight_durations.append(self.get_duration(journey_leg["duration"]))
            except KeyError:
                self.flight_durations.append("N/A")

        self.layovers = self.layovers[:-1]

        # Information for departure
        self.departure_airport_code = flight_details["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        try:
            self.departing_terminal = flight_details["itineraries"][0]["segments"][0]["departure"]["terminal"]
        except KeyError:
            self.departing_terminal = "N/A"
        departing_date_and_time = flight_details["itineraries"][0]["segments"][0]["departure"]["at"].split("T")
        self.departing_date = departing_date_and_time[0]
        self.departing_time = departing_date_and_time[1]

        # Information for arrival
        self.arrival_airport_code = flight_details["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        try:
            self.arrival_terminal = flight_details["itineraries"][0]["segments"][-1]["arrival"]["terminal"]
        except KeyError:
            self.arrival_terminal = "N/A"
        arrival_date_and_time = flight_details["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")
        self.arrival_date = arrival_date_and_time[0]
        self.arrival_time = arrival_date_and_time[1]

        if len(self.layovers) == 0:
            layovers = ""
            self.flight_durations = self.flight_durations[0]
        else:
            layovers = f"Layovers: {self.layovers}\n"

        formatted_text = (f"\nTrip {self.departure_airport_code} <---> {self.arrival_airport_code}: \n"
                          f"🏷️Price: CAD${self.price}\n"
                          f"Number of layovers: {len(self.layovers)}\n"
                          f"{layovers}Flight durations: {self.flight_durations}\n"
                          f"Total travel time: {self.duration}\n"
                          f"📆Departure date: {self.departing_date}\n"
                          f"🛫Departure at {self.departing_time} from terminal {self.departing_terminal}\n"
                          f"Arrival date: {self.arrival_date}\n"
                          f"🛬Arrival at {self.arrival_time} in terminal {self.arrival_terminal}\n"
                          f"Carriers: {self.carriers}\n"
                          f"Aircrafts: {self.aircraft}")

        print(formatted_text)


    def format_email(self):
        if len(self.layovers) == 0:
            layovers = ""
        else:
            layovers = f"Layovers: {self.layovers}\n"
        formatted_email = (f"{self.departure_airport_code} <---> {self.arrival_airport_code}\n"
                           f"Price: CAD${self.price}\n"
                           f"Total travel time: {self.duration}\n"
                           f"Departure date: {self.departing_date}\n"
                           f"Arrival date: {self.arrival_date}\n"
                           f"{layovers}Carriers: {self.carriers}"
        )

        return formatted_email