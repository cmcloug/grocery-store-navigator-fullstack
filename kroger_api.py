import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

token_url = "https://api.kroger.com/v1/connect/oauth2/token"
data = {
    "grant_type": "client_credentials",
    "scope": "product.compact"
}

response = requests.post(token_url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # <-- this shows Kroger’s full error

try:
    token_data = response.json()
    access_token = token_data["access_token"]
    print("Access Token:", access_token)
except KeyError:
    print("Failed to get access token. Full response JSON:", response.json())
