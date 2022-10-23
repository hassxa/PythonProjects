import datetime
import requests


APP_ID = "# Your APP ID in Nutritionix"
API_KEY = "# Your API KEY in Nutritionix"
API_SHEET = "# Your API Key in Sheety"

URL_NUTRITIONIX = "https://trackapi.nutritionix.com/v2/natural/exercise"
URL_SHEET = f"https://api.sheety.co/{API_SHEET}/myWorkouts/workouts"
QUERY = input("Tell me which exercises you did: ")
GENDER = "MALE"
WEIGHT_KG = 60
HEIGHT_CM = 180
AGE = 26

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

# Predict calories with Nutritionix
parameters = {
    "query": QUERY,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=URL_NUTRITIONIX, json=parameters, headers=headers)
response.raise_for_status()
result = response.json()


# POST in Google Sheet with basic authetication
USERNAME = "# Your username"
PASSWORD = "# Your password"
current_date = datetime.date.today().strftime("%d/%m/%Y")
current_time = datetime.datetime.now().strftime("%H:%M:%S")
exercises = result["exercises"]

for index in range(len(exercises)):
    sport = exercises[index]["name"].title()
    duration = exercises[index]["duration_min"]
    calories = exercises[index]["nf_calories"]
    row_content = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": sport,
            "duration": duration,
            "calories": calories
        }
    }
    response = requests.post(url=URL_SHEET, json=row_content, auth=(
                                                                   USERNAME,
                                                                   PASSWORD
    ))
    print(response.text)
