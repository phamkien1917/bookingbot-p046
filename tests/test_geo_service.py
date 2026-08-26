import pytest

from src.agents.nodes.inventory_agent import format_property_details_markdown
from src.agents.nodes.supervisor import _area_is_geo_target, _is_generic_geo_category_landmark
from src.services.geo_service import GeoService, has_valid_coordinates, haversine_km


def test_haversine_distance_is_reasonable() -> None:
    # Hồ Gươm -> Lăng Chủ tịch Hồ Chí Minh is roughly 2 km straight-line.
    distance = haversine_km(21.0285, 105.8542, 21.0368, 105.8347)
    assert 1.5 < distance < 2.5


def test_obviously_wrong_province_coordinate_is_rejected() -> None:
    assert has_valid_coordinates({
        "province": "Đà Nẵng",
        "latitude": 21.0285,
        "longitude": 105.8542,
    }) is False
    assert has_valid_coordinates({
        "province": "Đà Nẵng",
        "latitude": 16.0544,
        "longitude": 108.2022,
    }) is True


def test_commute_landmark_is_not_inventory_area() -> None:
    assert _area_is_geo_target(
        "Bệnh viện Bạch Mai",
        {"commute_landmark": "Bệnh viện Bạch Mai"},
    )
    assert _area_is_geo_target(
        "gần bệnh viện",
        {"nearby_categories": ["hospital"]},
    )
    assert not _area_is_geo_target(
        "Phường Bạch Mai",
        {"commute_landmark": "Bệnh viện Bạch Mai"},
    )


def test_generic_poi_category_is_not_treated_as_route_destination() -> None:
    assert _is_generic_geo_category_landmark("trường học")
    assert _is_generic_geo_category_landmark("trường học và bệnh viện")
    assert not _is_generic_geo_category_landmark("Bệnh viện Bạch Mai")


def test_geo_unavailable_details_do_not_echo_listing_claims() -> None:
    response = format_property_details_markdown(
        {
            "title": "Căn thử nghiệm",
            "list_price": 3_000_000_000,
            "area_sqm": 50,
            "bedrooms": 2,
            "bathrooms": 1,
            "description": "Cách Bệnh viện Bạch Mai 4 km, gần trường học.",
        },
        include_description=False,
    )

    assert "4 km" not in response
    assert "gần trường" not in response


@pytest.mark.asyncio
async def test_geo_local_cache_round_trip(monkeypatch: pytest.MonkeyPatch) -> None:
    async def no_redis():
        return None

    monkeypatch.setattr("src.services.geo_service.get_redis", no_redis)
    service = GeoService()
    await service._cache_set("geo:test", {"distance_km": 4.2}, ttl=60)

    assert await service._cache_get("geo:test") == {"distance_km": 4.2}
