"""Booking turns must not be read as commute limits.

An optional prefix on the hour pattern made "dat lich 10h" extract a
600-minute commute ceiling, which then steered intent classification in
supervisor_node for every booking turn.
"""

import pytest

from src.agents.nodes.supervisor import _extract_geo_constraints


@pytest.mark.parametrize("message", [
    "Toi muon dat lich 10h",
    "Dat lich xem nha luc 9h sang mai",
    "Toi muon xem can ho luc 14 gio chieu nay",
    "Toi ranh 2 tieng chieu nay",
])
def test_clock_times_are_not_commute_limits(message: str) -> None:
    assert "max_commute_minutes" not in _extract_geo_constraints(message)


@pytest.mark.parametrize("message,expected", [
    ("Tim nha di lam duoi 1 tieng", 60),
    ("Tim can ho cach benh vien Bach Mai duoi 15 phut", 15),
    ("Tim nha trong vong 30 phut di xe may", 30),
    ("Can ho khong qua 2 tieng den cong ty", 120),
])
def test_stated_limits_are_still_extracted(message: str, expected: int) -> None:
    assert _extract_geo_constraints(message)["max_commute_minutes"] == expected
