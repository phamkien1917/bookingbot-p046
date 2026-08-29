from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.services import route_optimizer
from src.services.route_optimizer import RoutePlan


def test_route_plan_exposes_grounding_and_feasibility() -> None:
    plan = RoutePlan(
        appointments=[],
        total_distance_km=0,
        total_duration_minutes=None,
        provider="HAVERSINE_FALLBACK",
        traffic_aware=False,
        feasible=True,
        legs=[],
        warnings=[],
    )
    assert plan.provider == "HAVERSINE_FALLBACK"
    assert plan.total_duration_minutes is None
    assert plan.feasible is True


@pytest.mark.asyncio
async def test_route_plan_flags_time_window_conflict(monkeypatch) -> None:
    first_start = datetime(2026, 8, 29, 2, tzinfo=UTC)
    first = SimpleNamespace(
        id=uuid4(), booking_code="BK-FIRST", starts_at=first_start,
        ends_at=first_start + timedelta(hours=1),
        property=SimpleNamespace(latitude=21.0, longitude=105.8),
    )
    second = SimpleNamespace(
        id=uuid4(), booking_code="BK-SECOND", starts_at=first.ends_at + timedelta(minutes=10),
        ends_at=first.ends_at + timedelta(hours=1, minutes=10),
        property=SimpleNamespace(latitude=21.1, longitude=105.9),
    )
    result = MagicMock()
    result.scalars.return_value.all.return_value = [first, second]
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)
    geo = SimpleNamespace(
        configured=True,
        settings=SimpleNamespace(geo_traffic_aware=True),
        route_matrix=AsyncMock(return_value={0: {"distance_km": 8.0, "duration_minutes": 30.0}}),
    )
    monkeypatch.setattr(route_optimizer, "get_geo_service", lambda: geo)

    plan = await route_optimizer.optimize_daily_route_plan(db, uuid4(), "2026-08-29")

    assert plan.provider == "Goong Distance Matrix"
    # Goong takes no departure time, so a grounded plan is still not traffic-aware.
    assert plan.traffic_aware is False
    assert plan.feasible is False
    assert plan.legs[0]["available_minutes"] == 10
    assert plan.warnings
