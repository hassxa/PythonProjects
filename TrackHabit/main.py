import requests
from datetime import datetime

USERNAME = "#Your Username"
TOKEN = "#Your Token"
GRAPH_ID = "#A graph ID"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# Create a user account
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)


graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_params = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "shibafu"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# Create the graph
# response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
# print(response.text)

pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now()

pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "26"
}

# Post a pixel
# response = requests.post(url=pixel_endpoint, json=pixel_params, headers=headers)
# print(response.text)

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

new_pixel_params = {
    "quantity": "4.5"
}

# Update a pixel
# response = requests.put(url=update_endpoint, json=new_pixel_params, headers=headers)
# print(response.text)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

# Delete a pixel
# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)

