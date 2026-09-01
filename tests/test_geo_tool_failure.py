"""Goong failing must never turn into a distance the agent claims anyway.

Fabricating a distance is the worst class of failure this product can produce:
the customer rides across Hanoi on a number nobody measured. The enrichment path
already drops evidence when the matrix call comes back empty, but nothing pinned
that behaviour down, so a future refactor could quietly start estimating.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.services.geo_service import GeoService


def two_properties() -> list[dict]:
    return [
        {"id": "p1", "title": "Căn A", "latitude": 21.0285, "longitude": 105.8542},
        {"id": "p2", "title": "Căn B", "latitude": 21.0333, "longitude": 105.7933},
    ]


@pytest.fixture
def configured_geo() -> GeoService:
    service = GeoService()
    with patch.object(GeoService, "configured", property(lambda self: True)):
        yield service


async def test_matrix_failure_leaves_no_distance_on_any_property(configured_geo):
    """route_matrix returns {} when every Goong chunk errors."""
    with (
        patch.object(GeoService, "geocode", AsyncMock(return_value=(21.03, 105.85))),
        patch.object(GeoService, "route_matrix", AsyncMock(return_value={})),
    ):
        result = await configured_geo.enrich_and_filter(
            two_properties(), destination="Hồ Gươm", travel_mode="TWO_WHEELER"
        )

    for item in result.properties:
        assert "distance_evidence" not in item, "no measurement means no claim"


async def test_matrix_failure_says_so_instead_of_going_quiet(configured_geo):
    with (
        patch.object(GeoService, "geocode", AsyncMock(return_value=(21.03, 105.85))),
        patch.object(GeoService, "route_matrix", AsyncMock(return_value={})),
    ):
        result = await configured_geo.enrich_and_filter(
            two_properties(), destination="Hồ Gươm", travel_mode="TWO_WHEELER"
        )

    assert result.note, "a silent drop reads to the customer as 'there is nothing nearby'"


async def test_geocode_failure_keeps_the_results_and_admits_it(configured_geo):
    """Goong cannot place the landmark: return the listings, unfiltered and unclaimed."""
    with patch.object(GeoService, "geocode", AsyncMock(return_value=None)):
        result = await configured_geo.enrich_and_filter(
            two_properties(), destination="Chỗ nào đó không có thật"
        )

    assert len(result.properties) == 2, "losing the listings punishes the customer for a tool outage"
    assert result.note and "Goong" in result.note
    assert not any("distance_evidence" in item for item in result.properties)


async def test_a_raising_matrix_does_not_produce_evidence(configured_geo):
    """A hard exception must surface, not be swallowed into a half-filled answer."""
    with (
        patch.object(GeoService, "geocode", AsyncMock(return_value=(21.03, 105.85))),
        patch.object(GeoService, "route_matrix", AsyncMock(side_effect=TimeoutError("Goong timeout"))),
    ):
        with pytest.raises(TimeoutError):
            await configured_geo.enrich_and_filter(two_properties(), destination="Hồ Gươm")


async def test_partial_results_only_keep_the_measured_ones(configured_geo):
    """Goong answered for one origin. The other must not inherit a number."""
    partial = {0: {"distance_km": 2.4, "duration_minutes": 9}}
    with (
        patch.object(GeoService, "geocode", AsyncMock(return_value=(21.03, 105.85))),
        patch.object(GeoService, "route_matrix", AsyncMock(return_value=partial)),
    ):
        result = await configured_geo.enrich_and_filter(
            two_properties(), destination="Hồ Gươm"
        )

    assert len(result.properties) == 1
    assert result.properties[0]["id"] == "p1"
    assert result.properties[0]["distance_evidence"]["distance_km"] == 2.4


async def test_evidence_names_its_provider():
    """A number the customer acts on has to say where it came from."""
    service = GeoService()
    with (
        patch.object(GeoService, "configured", property(lambda self: True)),
        patch.object(GeoService, "geocode", AsyncMock(return_value=(21.03, 105.85))),
        patch.object(
            GeoService,
            "route_matrix",
            AsyncMock(return_value={0: {"distance_km": 2.4, "duration_minutes": 9}}),
        ),
    ):
        result = await service.enrich_and_filter(two_properties()[:1], destination="Hồ Gươm")

    evidence = result.properties[0]["distance_evidence"]
    assert evidence["provider"] == "Goong Distance Matrix"
    assert evidence["destination"] == "Hồ Gươm"
