import argparse
import sys

from kroger_api import KrogerError, get_access_token, get_stores, search_product
from routing import build_route

DEFAULT_LIST = ["milk", "bread", "eggs", "chicken", "rice"]


def read_grocery_list(path):
    """Read one item per line from a file, or fall back to the default list."""
    if not path:
        return DEFAULT_LIST
    with open(path) as f:
        items = [line.strip() for line in f if line.strip()]
    return items or DEFAULT_LIST


def choose_store(stores):
    for i, s in enumerate(stores, 1):
        print(f"OPTION {i} {s['name']} — {s['address']}, {s['city']} (ID: {s['id']})")
    while True:
        choice = input("Enter your desired store number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(stores):
            return stores[int(choice) - 1]["id"]
        print(f"Please enter a number between 1 and {len(stores)}.")


def main():
    parser = argparse.ArgumentParser(description="Grocery Store Navigator")
    parser.add_argument("-l", "--list", help="text file with one grocery item per line")
    parser.add_argument("-z", "--zip", help="ZIP code to search near")
    args = parser.parse_args()

    print("🛒 Grocery Store Navigator\n")
    try:
        token = get_access_token()
        zip_code = args.zip or input("Enter your ZIP code: ").strip()
        stores = get_stores(token, zip_code)
        if not stores:
            print("❌ No stores found for that ZIP code.")
            return 1
        store_id = choose_store(stores)

        matches, not_found = [], []
        for item in read_grocery_list(args.list):
            print(f"🔍 Searching for: {item}...")
            products = search_product(token, item, store_id, limit=1).get("data", [])
            if not products:
                not_found.append(item)
                continue
            product = products[0]
            aisles = product.get("aisleLocations") or [None]
            matches.append((product["description"], aisles[0]))
    except (KrogerError, OSError) as exc:
        print(f"❌ {exc}")
        return 1

    route, unplaced = build_route(matches)
    print("\n🧭 Your route:")
    for aisle, names in route:
        print(f"  Aisle {aisle}: {', '.join(names)}")
    if unplaced:
        print(f"\n❓ No aisle info (check the store): {', '.join(unplaced)}")
    if not_found:
        print(f"\n❌ Not found: {', '.join(not_found)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
