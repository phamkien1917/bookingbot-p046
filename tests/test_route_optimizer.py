from datetime import UTC, date, datetime
from types import SimpleNamespace

import pytest

from src.services.route_optimizer import _local_day_bounds, _nearest_neighbour, haversine_distance


def appointment(identifier: str, latitude: float, longitude: float, hour: int):
    return SimpleNamespace(
        id=identifier,
        starts_at=datetime(2026, 8, 22, hour, tzinfo=UTC),
        property=SimpleNamespace(latitude=latitude, longitude=longitude),
    )


def test_haversine_distance_uses_kilometres() -> None:
    distance = haversine_distance(10.7769, 106.7009, 10.8231, 106.6297)
    assert distance == pytest.approx(9.3, abs=0.5)


def test_nearest_neighbour_does_not_modify_appointment_times() -> None:
    first = appointment("first", 10.7769, 106.7009, 1)
    far = appointment("far", 10.8231, 106.6297, 2)
    near = appointment("near", 10.7780, 106.7020, 3)
    original_times = {item.id: item.starts_at for item in (first, far, near)}

    result = _nearest_neighbour([first, far, near])

    assert [item.id for item in result] == ["first", "near", "far"]
    assert {item.id: item.starts_at for item in result} == original_times


def test_vietnamese_day_bounds_are_converted_to_utc() -> None:
    start, end = _local_day_bounds(date(2026, 8, 22))
    assert start == datetime(2026, 8, 21, 17, tzinfo=UTC)
    assert end == datetime(2026, 8, 22, 17, tzinfo=UTC)
