from flight_data import FlightData
from twilio.rest import Client
import smtplib
import os

# This class is responsible for sending notifications with the deal flight details.
class NotificationManager:
    def __init__(self):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(account_sid, auth_token)
        self.virtual_number = os.getenv("TWILIO_VIRTUAL_NUMBER")
        self.receiver_number = os.getenv("TWILIO_RECEIVER_NUMBER")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def send_message(self, price, origin, destination, departure_date, return_date):
        message = self.client.messages.create(
            from_=f"whatsapp:{self.virtual_number}",
            body=f"LOW PRICE ALERT!\n"
                 f"Only CAD${round(price, 2)} to fly from {origin} to {destination}\n"
                 f"Here are the details:\n"
                 f"Departure date: {departure_date}\n"
                 f"Arrival date: {return_date}",
            to=f"whatsapp:{self.receiver_number}"
        )

        print(message.status)

    def send_email(self, receiver_email, receiver_name, departing_flight_data, return_flight_data):
        departing_flight_email_body = departing_flight_data.format_email()
        return_flight_email_body = return_flight_data.format_email()

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.sender_email, password=self.email_password)
            connection.sendmail(
                from_addr=self.sender_email,
                msg=f"Subject: LOW PRICE ALERT!!!\n\n"
                    f"Hey {receiver_name},\n\n"
                    f"{departing_flight_email_body}\n\n"
                    f"{return_flight_email_body}\n\n"
                    f"---The Flight Club :)",
                to_addrs=receiver_email
            )