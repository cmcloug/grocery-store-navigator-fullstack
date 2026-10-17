import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.kroger.com/v1"
TIMEOUT = 10  # seconds


class KrogerError(Exception):
    """Raised when the Kroger API cannot be reached or returns an error."""


def _credentials():
    client_id = os.getenv("KROGER_CLIENT_ID")
    client_secret = os.getenv("KROGER_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise KrogerError(
            "Missing KROGER_CLIENT_ID / KROGER_CLIENT_SECRET. "
            "Copy .env.example to .env and fill in your credentials."
        )
    return client_id, client_secret


def _request(method, path, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.request(
            method, f"{BASE_URL}{path}", headers=headers, timeout=TIMEOUT, **kwargs
        )
    except requests.RequestException as exc:
        raise KrogerError(f"Network error contacting Kroger: {exc}") from exc
    if not response.ok:
        raise KrogerError(f"Kroger API error {response.status_code}: {response.text}")
    return response.json()


def get_access_token():
    """Retrieve an OAuth2 access token from Kroger."""
    data = _request(
        "POST",
        "/connect/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "scope": "product.compact"},
        auth=_credentials(),
    )
    token = data.get("access_token")
    if not token:
        raise KrogerError("Kroger response did not include an access token.")
    return token


def search_product(token, term, store_id, limit=3):
    """Search for a product by name within a specific store."""
    return _request(
        "GET",
        "/products",
        token,
        params={
            "filter.term": term,
            "filter.limit": limit,
            "filter.locationId": store_id,
        },
    )


def get_stores(token, zip_code, limit=5):
    """Return a list of nearby Kroger stores for a ZIP code."""
    data = _request(
        "GET",
        "/locations",
        token,
        params={"filter.zipCode.near": zip_code, "filter.limit": limit},
    )
    return [
        {
            "id": s["locationId"],
            "name": s.get("chain", "Kroger"),
            "address": s["address"]["addressLine1"],
            "city": s["address"]["city"],
        }
        for s in data.get("data", [])
    ]


def find_items(token, store_id, items):
    """Look up each item; return (matches, not_found) for routing.build_route."""
    matches, not_found = [], []
    for item in items:
        products = search_product(token, item, store_id, limit=1).get("data", [])
        if not products:
            not_found.append(item)
            continue
        product = products[0]
        aisles = product.get("aisleLocations") or [None]
        matches.append((product["description"], aisles[0]))
    return matches, not_found
