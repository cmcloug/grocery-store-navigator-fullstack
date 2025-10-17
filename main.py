import math
import itertools

# Define a mock store layout
store_layout = {
    "Aisle 1": {"coords": (0, 0), "items": ["milk", "yogurt", "cheese"]},
    "Aisle 2": {"coords": (1, 0), "items": ["bread", "bagels", "tortillas"]},
    "Aisle 3": {"coords": (2, 0), "items": ["bananas", "apples", "oranges"]},
    "Aisle 4": {"coords": (3, 0), "items": ["cereal", "oatmeal", "granola"]},
}

# Example grocery list
grocery_list = ["milk", "bananas", "bread", "cereal"]

# Match items to aisles
def find_item_locations(grocery_list, store_layout):
    locations = []
    for item in grocery_list:
        for aisle, data in store_layout.items():
            if item.lower() in [i.lower() for i in data["items"]]:
                locations.append((aisle, data["coords"]))
                break
    return locations

item_locations = find_item_locations(grocery_list, store_layout)

# Compute distance between two coordinates
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Find the best order (brute force, works fine for small lists)
def find_best_route(item_locations, start=(0, -1)):
    aisles = item_locations
    best_order = None
    best_distance = float("inf")
    for perm in itertools.permutations(aisles):
        total = 0
        current = start
        for _, coords in perm:
            total += distance(current, coords)
            current = coords
        if total < best_distance:
            best_distance = total
            best_order = perm
    return best_order, best_distance

best_route, total_dist = find_best_route(item_locations)

# Output results
print("🛒 Grocery List:", grocery_list)
print("\n📍 Aisle Assignments:")
for aisle, coords in item_locations:
    print(f"  - {aisle} ({coords})")

print("\n🚶 Optimal Route:")
for i, (aisle, _) in enumerate(best_route, 1):
    print(f"  Step {i}: Go to {aisle}")

print(f"\n🧭 Total walking distance: {total_dist:.2f} units")
