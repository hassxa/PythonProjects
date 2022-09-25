import requests
from datetime import datetime, timezone
import smtplib

MY_LAT = 0  # Your latitude
MY_LONG = 0  # Your longitude
MY_EMAIL = "YOUR_EMAIL@gmail.com"
MY_PASSWORD = "YOUR_PASSWORD"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.
iss_latitude_range = True if MY_LAT + 5 >= iss_latitude >= MY_LAT - 5 else False
iss_longitude_range = True if MY_LONG + 5 >= iss_longitude >= MY_LONG - 5 else False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now(timezone.utc)

is_dark = True if sunrise > time_now.hour > sunset else False


if iss_latitude_range and iss_longitude_range and is_dark:
    with smtplib.SMTP("smtp@gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="RECEIVER_EMAIL@gmail.com",
            msg="Subject:Look Up 👆\n\nThe ISS is above you in the sky!"
        )
