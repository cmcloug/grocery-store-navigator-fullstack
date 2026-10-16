"""Pure route-planning logic, kept free of network and I/O so it is easy to test."""
import re


def parse_aisle(aisle_location):
    """Return a sortable key for an aisle location dict, or None if unusable.

    Kroger aisle numbers are strings and are not always plain integers
    (e.g. "12", "12A"), so we sort numerically first, then by suffix.
    """
    raw = str((aisle_location or {}).get("number", "")).strip()
    match = re.match(r"(\d+)(.*)", raw)
    if not match:
        return None
    return int(match.group(1)), match.group(2).upper()


def build_route(matches):
    """Group (item, product_name, aisle_location) matches into an ordered route.

    Returns (route, unplaced) where route is a list of
    (aisle_label, [product names]) sorted by aisle, and unplaced lists
    products found without usable aisle information.
    """
    by_aisle = {}
    unplaced = []
    for product_name, aisle_location in matches:
        key = parse_aisle(aisle_location)
        if key is None:
            unplaced.append(product_name)
        else:
            by_aisle.setdefault(key, []).append(product_name)
    route = [(f"{n}{suffix}", by_aisle[(n, suffix)]) for n, suffix in sorted(by_aisle)]
    return route, unplaced
