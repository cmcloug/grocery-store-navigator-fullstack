import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from routing import build_route, parse_aisle


def test_parse_aisle_handles_suffix_and_garbage():
    assert parse_aisle({"number": "12A"}) == (12, "A")
    assert parse_aisle({"number": "7"}) == (7, "")
    assert parse_aisle({"number": "Frozen"}) is None
    assert parse_aisle(None) is None


def test_build_route_sorts_groups_and_reports_unplaced():
    matches = [
        ("Eggs", {"number": "10"}),
        ("Milk", {"number": "2"}),
        ("Butter", {"number": "2"}),
        ("Rice", {"number": "10A"}),
        ("Mystery", None),
    ]
    route, unplaced = build_route(matches)
    assert route == [("2", ["Milk", "Butter"]), ("10", ["Eggs"]), ("10A", ["Rice"])]
    assert unplaced == ["Mystery"]
