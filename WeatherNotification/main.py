import requests
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = "#Your API Key"
ACCOUNT_SID = "#Your Account ID"
AUTH_TOKEN = "#Your Authentication Token"
MY_LAT = "#Your Latitude"
MY_LONG = "#Your Longitude"
NEXT_HOURS = 12

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

is_going_to_rain = False

for hour in range(NEXT_HOURS):
    code = weather_data["hourly"][hour]["weather"][0]["id"]
    if code < 700:
        is_going_to_rain = True

if is_going_to_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂️.",
        from_='#Your Twilio Phone Number',
        to='#Your phone number (+xxx)'
    )
    print(message.status)
