"""Small HTTP API so the frontend can use the Kroger lookup and route planning."""
import time

from flask import Flask, jsonify, request

from kroger_api import KrogerError, find_items, get_access_token, get_stores
from routing import build_route

app = Flask(__name__)

_token = {"value": None, "expires": 0.0}
TOKEN_TTL = 25 * 60  # Kroger tokens last 30 minutes


def token():
    if not _token["value"] or time.time() > _token["expires"]:
        _token["value"] = get_access_token()
        _token["expires"] = time.time() + TOKEN_TTL
    return _token["value"]


@app.errorhandler(KrogerError)
def kroger_error(exc):
    return jsonify(error=str(exc)), 502


@app.get("/api/stores")
def stores():
    zip_code = request.args.get("zip", "").strip()
    if not (zip_code.isdigit() and len(zip_code) == 5):
        return jsonify(error="Enter a valid 5-digit ZIP code."), 400
    return jsonify(stores=get_stores(token(), zip_code))


@app.post("/api/route")
def route():
    body = request.get_json(silent=True) or {}
    store_id = body.get("store_id")
    items = [i.strip() for i in body.get("items", []) if isinstance(i, str) and i.strip()]
    if not store_id or not items:
        return jsonify(error="store_id and at least one item are required."), 400
    matches, not_found = find_items(token(), store_id, items)
    route_, unplaced = build_route(matches)
    return jsonify(
        route=[{"aisle": a, "items": names} for a, names in route_],
        unplaced=unplaced,
        not_found=not_found,
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
