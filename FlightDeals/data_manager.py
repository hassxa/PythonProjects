import requests
import datetime
from twilio.rest import Client
from secrets_id import SHEETY_ENDPOINT, TEQUILA_ENDPOINT, TEQUILA_URL, ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, \
    PERSONAL_PHONE


class DataManager:

    def __init__(self):
        self.data = {}
        self.data_flight = None
        self.best_prices = None
        self.cheap_trip = None

    def get_city(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        data_prices = response.json()["prices"]
        self.data = data_prices
        return self.data

    @staticmethod
    def get_iata_code(city_name):
        headers = {
            "apikey": TEQUILA_ENDPOINT
        }
        parameters = {
            "term": city_name
        }
        response = requests.get(url=f"{TEQUILA_URL}locations/query", params=parameters, headers=headers)
        data_code = response.json()["locations"][0]["code"]
        return data_code

    @staticmethod
    def update_data(iata_code, city_id):
        new_data = {
            "price": {
                "iataCode": iata_code
            }
        }
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{city_id}", json=new_data)
        print(response.text)

    def cheap_flight(self, origin_airport, iata_code_dest, city_name, lowest_price):
        headers = {
            "apikey": TEQUILA_ENDPOINT
        }
        parameters_search_flights = {
            "fly_from": origin_airport,
            "fly_to": iata_code_dest,
            "date_from": (datetime.date.today() + datetime.timedelta(1)).strftime("%d/%m/%Y"),
            "date_to": (datetime.date.today() + datetime.timedelta(6 * 30)).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"
        }
        response = requests.get(url=f"{TEQUILA_URL}v2/search", params=parameters_search_flights, headers=headers)
        self.data_flight = response.json()
        try:
            self.best_prices = self.data_flight["data"][0]["price"]
            self.cheap_trip = True if self.best_prices < lowest_price else False
            print(f"{city_name}: €{self.best_prices}")
        except IndexError:
            print(f"No existen vuelos entre {origin_airport} y {iata_code_dest}")

    def send_sms(self):
        if self.cheap_trip:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages \
                .create(
                body=f"¡Alerta de vuelo barato!\nSolo {self.best_prices}€ por volar de "
                     f"{self.data_flight['data'][0]['cityFrom']}-{self.data_flight['data'][0]['flyFrom']} "
                     f"a {self.data_flight['data'][0]['cityTo']}-{self.data_flight['data'][0]['flyTo']} "
                     f"desde {(self.data_flight['data'][0]['route'][0]['local_departure']).split('T')[0]} hasta "
                     f"{(self.data_flight['data'][0]['route'][1]['local_arrival']).split('T')[0]}",
                from_=TWILIO_PHONE,
                to=PERSONAL_PHONE
            )
            print(message.status)
