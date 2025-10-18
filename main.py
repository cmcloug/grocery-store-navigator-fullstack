from kroger_api import get_access_token, search_product, find_store

def main():
    print("🛒 Grocery Store Navigator - Kroger API Demo\n")

    token = get_access_token()
    if not token:
        print("❌ Failed to get access token. Check your credentials.")
        return
    print("✅ Access token acquired!\n")

    zip_code = input("Enter your ZIP code to find nearby Kroger stores: ")
    store_id = find_store(token, zip_code)
    if not store_id:
        return

    grocery_list = ["milk", "bread", "eggs", "chicken", "rice"]

    for item in grocery_list:
        print(f"\n🔍 Searching for: {item}...")
        results = search_product(token, item, store_id)

        if "data" not in results or not results["data"]:
            print(f"❌ No results found for '{item}'")
            continue

        for product in results["data"][:1]:
            name = product["description"]
            aisle = "N/A"
            try:
                aisle_data = product["aisleLocations"][0]
                aisle = aisle_data.get("number", "N/A")
            except (KeyError, IndexError):
                pass

            print(f"🛍️  {name} — Aisle: {aisle}")

if __name__ == "__main__":
    main()
