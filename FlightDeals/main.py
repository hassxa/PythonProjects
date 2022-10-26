import requests
import datetime
from twilio.rest import Client

SHEETY_ENDPOINT = "#Sheety Endpoint"
TEQUILA_ENDPOINT = "#Tequila Endpoint"
TEQUILA_URL = "#Tequila URL"
ACCOUNT_SID = "#Twilio Account ID"
AUTH_TOKEN = "#Twilio Auth Token"
TWILIO_PHONE_NUMBER = "#Twilio Phone Number"

# Obtener nombres ciudades de Google Sheet
response = requests.get(url=SHEETY_ENDPOINT)
cities_data = response.json()["prices"]

# Obtener código IATA de las ciudades de Google Sheet
headers = {
    "apikey": TEQUILA_ENDPOINT
}
for city_data in cities_data:
    parameters_iata_code = {
        "term": city_data["city"]
    }
    response = requests.get(url=f"{TEQUILA_URL}/locations/query", params=parameters_iata_code, headers=headers)
    iata_code = response.json()["locations"][0]["code"]

    # Función que rellena código IATA a las ciudades destinos en Google Sheet
    new_data = {
        "price": {
            "iataCode": iata_code
        }
    }
    response = requests.put(url=f"{SHEETY_ENDPOINT}/{city_data['id']}", json=new_data)
    print(response.text)

    # Buscar vuelos baratos
    ORIGIN_AIRPORT = "AGP"
    parameters_search_flights = {
        "fly_from": ORIGIN_AIRPORT,
        "fly_to": iata_code,
        "date_from": (datetime.date.today() + datetime.timedelta(1)).strftime("%d/%m/%Y"),
        "date_to": (datetime.date.today() + datetime.timedelta(6*30)).strftime("%d/%m/%Y"),
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "flight_type": "round",
        "one_for_city": 1,
        "max_stopovers": 0,
        "curr": "EUR"
    }
    response = requests.get(url=f"{TEQUILA_URL}/v2/search", params=parameters_search_flights, headers=headers)
    data = response.json()
    try:
        best_prices = data["data"][0]["price"]
        cheap_trip = True if best_prices < city_data['lowestPrice'] else False
        print(f"{city_data['city']}: €{best_prices}")
    except IndexError:
        print(f"No existen vuelos entre {ORIGIN_AIRPORT} y {iata_code}")
    else:
        if cheap_trip:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages \
                .create(
                body=f"¡Alerta de vuelo barato!\nSolo {best_prices}€ por volar de {data['data'][0]['cityFrom']}-"
                     f"{data['data'][0]['flyFrom']} a {data['data'][0]['cityTo']}-{data['data'][0]['flyTo']} "
                     f"desde {(data['data'][0]['route'][0]['local_departure']).split('T')[0]} hasta "
                     f"{(data['data'][0]['route'][1]['local_arrival']).split('T')[0]}",
                from_=TWILIO_PHONE_NUMBER,
                to='#Your personal phone number'
            )
            print(message.status)
