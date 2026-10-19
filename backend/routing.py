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


def _int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _is_department(description):
    """Kroger labels regular aisles "AISLE 7"; anything else (DAIRY, MEAT) is a department."""
    description = (description or "").strip().upper()
    return bool(description) and not description.startswith("AISLE")


def build_route(matches):
    """Group (product_name, aisle_location) matches into an ordered route.

    Returns (route, unplaced). route is a list of stops sorted by aisle:
    {label, number, department, items: [{name, bay, side}]}, with each stop's
    items ordered front-to-back by bay. unplaced lists products found
    without usable aisle information.
    """
    stops = {}
    unplaced = []
    for product_name, location in matches:
        key = parse_aisle(location)
        if key is None:
            unplaced.append(product_name)
            continue
        number, suffix = key
        description = (location.get("description") or "").strip()
        department = _is_department(description)
        stop = stops.setdefault(
            key,
            {
                "label": description.title() if department else f"Aisle {number}{suffix}",
                "number": number,
                "department": department,
                "items": [],
            },
        )
        stop["items"].append(
            {
                "name": product_name,
                "bay": _int_or_none(location.get("bayNumber")),
                "side": location.get("side"),
            }
        )
    route = [stops[k] for k in sorted(stops)]
    for stop in route:
        stop["items"].sort(key=lambda i: (i["bay"] is None, i["bay"] or 0))
    return route, unplaced
