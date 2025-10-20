import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

def get_access_token():
    """Retrieve an OAuth2 access token from Kroger."""
    url = "https://api.kroger.com/v1/connect/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }

    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    if response.status_code != 200:
        print("❌ Failed to get token:", response.status_code, response.text)
        return None

    token_data = response.json()
    access_token = token_data.get("access_token")
    print("✅ Access token received.")
    return access_token

def search_product(token, term, store_id, limit=3):
    """Search for a product by name within a specific store."""
    url = "https://api.kroger.com/v1/products"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "filter.term": term,
        "filter.limit": limit,
        "filter.locationId": store_id
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def find_store(token, zip_code):
    """Find nearby Kroger stores using a ZIP code."""
    url = "https://api.kroger.com/v1/locations"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "filter.zipCode.near": zip_code,
        "filter.limit": 5 
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "data" not in data or not data["data"]:
        print("❌ No stores found for that ZIP code.")
        return None

    # Print store options
    choice_num = 1
    choice_list = []
    for store in data["data"]:
        name = store["chain"]
        address = store["address"]["addressLine1"]
        city = store["address"]["city"]
        store_id = store["locationId"]
        print(f"OPTION {choice_num} {name} — {address}, {city} (ID: {store_id})")
        choice_list.append(store_id)
        choice_num += 1

    choice = input("Enter your desired store location choice number: ")
    chosen = int(choice)
    # Return the first store ID
    return choice_list[chosen - 1]

