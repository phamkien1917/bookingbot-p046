"""Geo maths and the Goong client, with no network and no API key spent.

Commute time is the one number in a listing card that does not come from the
database — it comes from a paid third party, over a network, and it is the
number a buyer decides on. So the failure modes matter more than the happy path:
a malformed response, a coordinate in the wrong province, a batch too large for
one request.

`tests/test_geo_tool_failure.py` already pins that an outage never fabricates a
distance. This file covers the layer beneath it.
"""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from src.services.geo_service import GeoService, has_valid_coordinates, haversine_km


class TestHaversine:
    def test_a_known_distance_comes_out_right(self):
        """Hoàn Kiếm to Bến Thành is about 1,140 km in a straight line."""
        km = haversine_km(21.0285, 105.8542, 10.7769, 106.7009)

        assert 1130 < km < 1160, f"got {km:.0f} km"

    def test_a_short_hop_inside_one_district(self):
        """Cầu Giấy to Ba Đình, roughly 4 km."""
        km = haversine_km(21.0313, 105.7965, 21.0333, 105.8342)

        assert 3 < km < 5, f"got {km:.2f} km"

    def test_the_same_point_is_zero_away_from_itself(self):
        assert haversine_km(21.0285, 105.8542, 21.0285, 105.8542) == pytest.approx(0, abs=1e-9)

    def test_the_measurement_does_not_depend_on_direction(self):
        there = haversine_km(21.0285, 105.8542, 10.7769, 106.7009)
        back = haversine_km(10.7769, 106.7009, 21.0285, 105.8542)

        assert there == pytest.approx(back)


class TestHasValidCoordinates:
    """A bad coordinate produces a confident, wrong commute time."""

    def test_a_hanoi_listing_with_hanoi_coordinates_passes(self):
        assert has_valid_coordinates(
            {"latitude": 21.0285, "longitude": 105.8542, "province": "Hà Nội"}
        )

    def test_a_coordinate_outside_vietnam_is_rejected(self):
        """Geocoders answer for the whole planet; the inventory is one country."""
        assert not has_valid_coordinates({"latitude": 48.8584, "longitude": 2.2945})

    def test_a_hanoi_listing_sitting_in_saigon_is_rejected(self):
        """The commonest crawl defect: right city name, wrong point."""
        assert not has_valid_coordinates(
            {"latitude": 10.7769, "longitude": 106.7009, "province": "Hà Nội"}
        )

    @pytest.mark.parametrize(
        "item",
        [
            {},
            {"latitude": None, "longitude": None},
            {"latitude": "", "longitude": ""},
            {"latitude": "không rõ", "longitude": "không rõ"},
            {"latitude": 21.0285},
        ],
    )
    def test_anything_unusable_is_rejected_rather_than_guessed(self, item):
        assert not has_valid_coordinates(item)

    def test_a_province_nobody_mapped_is_allowed_through(self):
        """An unknown province means no bounds to check, not an automatic no."""
        assert has_valid_coordinates(
            {"latitude": 16.0544, "longitude": 108.2022, "province": "Tỉnh Chưa Có Trong Bảng"}
        )


class TestCacheKey:
    def test_the_same_payload_gives_the_same_key_whatever_the_order(self):
        a = GeoService._cache_key("geocode", {"lat": 1, "lon": 2})
        b = GeoService._cache_key("geocode", {"lon": 2, "lat": 1})

        assert a == b

    def test_two_namespaces_do_not_collide(self):
        payload = {"lat": 1, "lon": 2}

        assert GeoService._cache_key("geocode", payload) != GeoService._cache_key("route", payload)


def goong_response(payload: dict, status_code: int = 200):
    """Stand in for what httpx hands back from rsapi.goong.io."""
    return SimpleNamespace(
        status_code=status_code,
        json=lambda: payload,
        raise_for_status=lambda: None,
        text=json.dumps(payload),
    )


def patched_client(response):
    """Patch httpx.AsyncClient so no request leaves the machine."""
    client = AsyncMock()
    client.get = AsyncMock(return_value=response)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)
    return patch("src.services.geo_service.httpx.AsyncClient", return_value=client)


class TestGeocode:
    @pytest.mark.asyncio
    async def test_a_good_answer_is_read_out_correctly(self):
        service = GeoService()
        service._cache_get = AsyncMock(return_value=None)
        service._cache_set = AsyncMock()
        payload = {
            "status": "OK",
            "results": [{"geometry": {"location": {"lat": 21.0285, "lng": 105.8542}}}],
        }

        with patched_client(goong_response(payload)):
            result = await service.geocode("Hồ Hoàn Kiếm")

        assert result == (21.0285, 105.8542)

    @pytest.mark.asyncio
    async def test_an_address_goong_cannot_place_returns_nothing(self):
        """None means "unknown". Any coordinate here would be invented."""
        service = GeoService()
        service._cache_get = AsyncMock(return_value=None)
        service._cache_set = AsyncMock()

        with patched_client(goong_response({"status": "ZERO_RESULTS", "results": []})):
            assert await service.geocode("một nơi không tồn tại") is None

    @pytest.mark.asyncio
    async def test_a_result_missing_its_location_returns_nothing(self):
        """A malformed payload must not become a coordinate of (0, 0)."""
        service = GeoService()
        service._cache_get = AsyncMock(return_value=None)
        service._cache_set = AsyncMock()

        with patched_client(goong_response({"status": "OK", "results": [{"geometry": {}}]})):
            assert await service.geocode("Cầu Giấy") is None

    @pytest.mark.asyncio
    async def test_a_cached_address_is_not_asked_for_again(self):
        """Geocoding is billed per call; the same address twice is one call."""
        service = GeoService()
        service._cache_get = AsyncMock(return_value=[21.0285, 105.8542])

        with patched_client(goong_response({})) as mock_client:
            result = await service.geocode("Hồ Hoàn Kiếm")

        assert result == (21.0285, 105.8542)
        mock_client.assert_not_called()


class TestConfigured:
    def test_no_api_key_means_not_configured(self):
        """The whole geo layer must be able to report that it is switched off."""
        service = GeoService()
        service.settings = SimpleNamespace(goong_api_key="")

        assert service.configured is False

    def test_a_key_means_configured(self):
        service = GeoService()
        service.settings = SimpleNamespace(goong_api_key="a-key")

        assert service.configured is True
