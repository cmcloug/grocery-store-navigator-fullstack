import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from routing import build_route, parse_aisle


def test_parse_aisle_handles_suffix_and_garbage():
    assert parse_aisle({"number": "12A"}) == (12, "A")
    assert parse_aisle({"number": "7"}) == (7, "")
    assert parse_aisle({"number": "Frozen"}) is None
    assert parse_aisle(None) is None


def loc(number, description=None, bay=None, side=None):
    d = {"number": number}
    if description:
        d["description"] = description
    if bay:
        d["bayNumber"] = bay
    if side:
        d["side"] = side
    return d


def test_build_route_sorts_groups_and_reports_unplaced():
    matches = [
        ("Eggs", loc("10", "AISLE 10")),
        ("Milk", loc("2", "AISLE 2", bay="9")),
        ("Butter", loc("2", "AISLE 2", bay="3")),
        ("Rice", loc("10A")),
        ("Mystery", None),
    ]
    route, unplaced = build_route(matches)
    assert [s["label"] for s in route] == ["Aisle 2", "Aisle 10", "Aisle 10A"]
    # items in an aisle are ordered by bay, front to back
    assert [i["name"] for i in route[0]["items"]] == ["Butter", "Milk"]
    assert unplaced == ["Mystery"]


def test_departments_are_labelled_by_description():
    route, _ = build_route(
        [("Bananas", loc("0", "FRUIT")), ("Milk", loc("100", "DAIRY", "30", "L"))]
    )
    assert [(s["label"], s["department"]) for s in route] == [
        ("Fruit", True),
        ("Dairy", True),
    ]
    assert route[1]["items"][0] == {"name": "Milk", "bay": 30, "side": "L"}
