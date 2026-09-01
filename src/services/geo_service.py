"""Grounded distance, travel-time and nearby-amenity enrichment.

Google data is only attached when the provider returns evidence. The caller can
surface ``note`` when configuration, coordinates, or provider data is missing.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import math
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from src.config import get_settings
from src.services.chat_state_service import normalize_text
from src.services.redis_service import get_redis

logger = logging.getLogger(__name__)

TRAVEL_MODES = {"DRIVE", "WALK", "BICYCLE", "TRANSIT", "TWO_WHEELER"}
PLACE_TYPES = {
    "school": ["school", "primary_school", "secondary_school"],
    "hospital": ["hospital", "medical_center"],
    "university": ["university"],
    "supermarket": ["supermarket"],
    "park": ["park"],
}

GEO_NOT_CONFIGURED_NOTE = (
    "Chưa thể xác minh khoảng cách/tiện ích vì Geo Service chưa được cấu hình."
)
GEO_NO_BASE_RESULTS_NOTE = (
    "Kho dữ liệu chưa có tin phù hợp tiêu chí cơ bản, nên chưa thể xác minh "
    "khoảng cách/tiện ích cho yêu cầu này."
)

# Broad validation boxes catch obvious cross-province crawler errors without
# pretending to be administrative-boundary geometry.
PROVINCE_BOUNDS = {
    "ha noi": (20.50, 21.40, 105.20, 106.10),
    "ho chi minh": (10.30, 11.20, 106.30, 107.10),
    "da nang": (15.85, 16.35, 107.80, 108.55),
    "khanh hoa": (11.80, 12.90, 108.60, 109.50),
    "quang ninh": (20.70, 21.70, 106.40, 108.10),
    "binh duong": (10.80, 11.55, 106.30, 107.10),
}


@dataclass
class GeoSearchResult:
    properties: list[dict[str, Any]]
    note: str | None = None
    provider: str | None = None
    filtered: bool = False


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    value = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def has_valid_coordinates(item: dict[str, Any]) -> bool:
    try:
        lat = float(item["latitude"])
        lon = float(item["longitude"])
    except (KeyError, TypeError, ValueError):
        return False
    if not (8 <= lat <= 24 and 102 <= lon <= 110):
        return False
    province = normalize_text(str(item.get("province") or ""))
    bounds = PROVINCE_BOUNDS.get(province)
    if not bounds:
        return True
    min_lat, max_lat, min_lon, max_lon = bounds
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon


class GeoService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._local_cache: dict[str, tuple[float, str]] = {}

    @property
    def configured(self) -> bool:
        return bool(self.settings.goong_api_key)

    @staticmethod
    def _cache_key(namespace: str, payload: Any) -> str:
        serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return f"geo:{namespace}:{digest}"

    async def _cache_get(self, key: str) -> Any | None:
        local = self._local_cache.get(key)
        if local:
            expires_at, payload = local
            if expires_at > time.time():
                return json.loads(payload)
            self._local_cache.pop(key, None)

        try:
            client = await get_redis()
            if client is None:
                return None
            payload = await client.get(key)
            if payload is None:
                return None
            if isinstance(payload, bytes):
                payload = payload.decode("utf-8")
            return json.loads(payload)
        except Exception as exc:
            logger.debug("Geo cache read failed for %s: %s", key, exc)
            return None

    async def _cache_set(self, key: str, value: Any, ttl: int) -> None:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        self._local_cache[key] = (time.time() + ttl, payload)
        try:
            client = await get_redis()
            if client is not None:
                await client.set(key, payload, ex=ttl)
        except Exception as exc:
            logger.debug("Geo cache write failed for %s: %s", key, exc)

    async def geocode(self, address: str) -> tuple[float, float] | None:
        cache_key = self._cache_key("geocode", normalize_text(address))
        cached = await self._cache_get(cache_key)
        if isinstance(cached, list) and len(cached) == 2:
            return float(cached[0]), float(cached[1])

        async with httpx.AsyncClient(timeout=self.settings.geo_timeout_seconds) as client:
            response = await client.get(
                "https://rsapi.goong.io/Geocode",
                params={
                    "address": f"{address}, Việt Nam",
                    "api_key": self.settings.goong_api_key,
                },
            )
            response.raise_for_status()
            payload = response.json()
        if payload.get("status") != "OK" or not payload.get("results"):
            return None
        location = payload["results"][0].get("geometry", {}).get("location", {})
        try:
            coordinates = float(location["lat"]), float(location["lng"])
        except (KeyError, TypeError, ValueError):
            return None
        await self._cache_set(
            cache_key,
            list(coordinates),
            self.settings.geo_geocode_cache_ttl_seconds,
        )
        return coordinates

    async def route_matrix(
        self,
        origins: list[tuple[float, float]],
        destination: tuple[float, float],
        travel_mode: str,
        departure_time: datetime | None = None,
    ) -> dict[int, dict[str, float]]:
        mode = travel_mode if travel_mode in TRAVEL_MODES else "DRIVE"
        cache_key = self._cache_key(
            "route_matrix",
            {
                "origins": [[round(lat, 6), round(lon, 6)] for lat, lon in origins],
                "destination": [round(destination[0], 6), round(destination[1], 6)],
                "travel_mode": mode,
            },
        )
        cached = await self._cache_get(cache_key)
        if isinstance(cached, dict):
            return {int(index): evidence for index, evidence in cached.items()}

        # Goong only offers car and bike. Walking and transit are served by the
        # nearest available profile, so their durations are approximations.
        # ponytail: swap in a walking-capable provider if pedestrian ETAs start to matter.
        mode_mapping = {"DRIVE": "car", "TWO_WHEELER": "bike", "WALK": "bike", "BICYCLE": "bike", "TRANSIT": "car"}
        vehicle = mode_mapping.get(mode, "car")
        dest_str = f"{destination[0]},{destination[1]}"
        result: dict[int, dict[str, float]] = {}

        chunk_size = 10
        async with httpx.AsyncClient(timeout=self.settings.geo_timeout_seconds) as client:
            for offset in range(0, len(origins), chunk_size):
                chunk = origins[offset:offset + chunk_size]
                origins_str = "|".join(f"{lat},{lon}" for lat, lon in chunk)
                try:
                    response = await client.get(
                        "https://rsapi.goong.io/DistanceMatrix",
                        params={
                            "origins": origins_str,
                            "destinations": dest_str,
                            "vehicle": vehicle,
                            "api_key": self.settings.goong_api_key,
                        },
                    )
                    response.raise_for_status()
                    payload = response.json()
                    rows = payload.get("rows", [])
                    for i, row in enumerate(rows):
                        elements = row.get("elements", [])
                        if not elements:
                            continue
                        element = elements[0]
                        if element.get("status") == "OK":
                            distance_m = element.get("distance", {}).get("value")
                            duration_s = element.get("duration", {}).get("value")
                            if distance_m is not None and duration_s is not None:
                                result[offset + i] = {
                                    "distance_km": round(float(distance_m) / 1000, 2),
                                    "duration_minutes": round(float(duration_s) / 60, 1),
                                }
                except Exception as exc:
                    logger.warning(f"Goong DistanceMatrix chunk {offset} failed: {exc}")
        await self._cache_set(
            cache_key,
            {str(index): evidence for index, evidence in result.items()},
            self.settings.geo_route_cache_ttl_seconds,
        )
        return result

    async def nearby_places(
        self,
        origin: tuple[float, float],
        categories: list[str],
        radius_m: float = 3000,
    ) -> list[dict[str, Any]]:
        included = sorted({place_type for category in categories for place_type in PLACE_TYPES.get(category, [])})
        if not included:
            return []
        places = []
        async with httpx.AsyncClient(timeout=self.settings.geo_timeout_seconds) as client:
            for keyword in included:
                try:
                    response = await client.get(
                        "https://rsapi.goong.io/Place/NearbySearch",
                        params={
                            "location": f"{origin[0]},{origin[1]}",
                            "radius": radius_m,
                            "keyword": keyword.replace("_", " "),
                            "api_key": self.settings.goong_api_key,
                        }
                    )
                    response.raise_for_status()
                    payload = response.json()
                    for place in payload.get("results", [])[:5]:
                        location = place.get("geometry", {}).get("location", {})
                        try:
                            distance = haversine_km(
                                origin[0], origin[1], float(location.get("lat", 0)), float(location.get("lng", 0))
                            )
                        except (KeyError, TypeError, ValueError):
                            continue
                        places.append({
                            "name": place.get("name", "Địa điểm"),
                            "category": keyword,
                            "straight_line_km": round(distance, 2),
                        })
                except httpx.HTTPError as exc:
                    logger.warning("Goong nearby search failed for %s: %s", keyword, exc)
        return places

    async def diagnose_capabilities(self) -> dict[str, Any]:
        """Make small real provider calls without ever returning the API key."""
        if not self.configured:
            return {
                "configured": False,
                "fully_operational": False,
                "capabilities": {},
            }

        capabilities: dict[str, dict[str, Any]] = {}

        try:
            target = await self.geocode("Bệnh viện Bạch Mai, Hà Nội")
            capabilities["geocoding"] = {
                "operational": target is not None,
                "status": "OK" if target else "NO_RESULT_OR_REQUEST_DENIED",
            }
        except httpx.HTTPError as exc:
            capabilities["geocoding"] = self._diagnostic_http_failure(exc)

        try:
            routes = await self.route_matrix(
                [(21.0285, 105.8542)],
                (21.0008, 105.8411),
                "DRIVE",
            )
            capabilities["routes"] = {
                "operational": bool(routes),
                "status": "OK" if routes else "NO_ROUTE_OR_REQUEST_DENIED",
            }
        except httpx.HTTPError as exc:
            capabilities["routes"] = self._diagnostic_http_failure(exc)

        try:
            places = await self.nearby_places(
                (21.0008, 105.8411),
                ["hospital"],
            )
            capabilities["places"] = {
                "operational": bool(places),
                "status": "OK" if places else "NO_RESULT_OR_REQUEST_DENIED",
            }
        except httpx.HTTPError as exc:
            capabilities["places"] = self._diagnostic_http_failure(exc)

        return {
            "configured": True,
            "fully_operational": all(
                item.get("operational", False) for item in capabilities.values()
            ),
            "capabilities": capabilities,
        }

    @staticmethod
    def _diagnostic_http_failure(exc: httpx.HTTPError) -> dict[str, Any]:
        result: dict[str, Any] = {
            "operational": False,
            "status": type(exc).__name__,
        }
        if isinstance(exc, httpx.HTTPStatusError):
            result["http_status"] = exc.response.status_code
            try:
                payload = exc.response.json()
                error = payload.get("error", {}) if isinstance(payload, dict) else {}
                if isinstance(error, dict) and error.get("status"):
                    result["provider_status"] = error["status"]
            except ValueError:
                pass
        return result

    async def enrich_and_filter(self, *args: Any, **kwargs: Any) -> GeoSearchResult:
        """Time the Goong round-trip so it can be told apart from the LLM cost.

        The graph's per-node timing lumps this external call in with the
        inventory LLM call; this line reports the geo portion on its own.
        """
        started = time.perf_counter()
        try:
            return await self._enrich_and_filter(*args, **kwargs)
        finally:
            logger.info("geo.enrich_and_filter took %d ms", round((time.perf_counter() - started) * 1000))

    async def _enrich_and_filter(
        self,
        properties: list[dict[str, Any]],
        *,
        destination: str | None,
        destination_coordinates: tuple[float, float] | None = None,
        travel_mode: str = "DRIVE",
        max_km: float | None = None,
        max_minutes: int | None = None,
        nearby_categories: list[str] | None = None,
    ) -> GeoSearchResult:
        categories = [category for category in (nearby_categories or []) if category in PLACE_TYPES]
        if not destination and not destination_coordinates and not categories:
            return GeoSearchResult(properties)
        if not self.configured:
            return GeoSearchResult(properties, GEO_NOT_CONFIGURED_NOTE)

        valid = [item for item in properties if has_valid_coordinates(item)]
        if not valid:
            return GeoSearchResult(
                properties,
                "Không có tọa độ đã vượt qua kiểm tra chất lượng; chưa áp dụng tiêu chí địa lý.",
            )

        try:
            if destination or destination_coordinates:
                target = destination_coordinates or await self.geocode(str(destination))
                if not target:
                    return GeoSearchResult(
                        properties,
                        f"Chưa thể xác minh vị trí ‘{destination}’ bằng Goong; "
                        "kết quả chưa được lọc theo khoảng cách/thời gian.",
                    )
                routes = await self.route_matrix(
                    [(float(item["latitude"]), float(item["longitude"])) for item in valid],
                    target,
                    travel_mode,
                )
                for index, item in enumerate(valid):
                    evidence = routes.get(index)
                    if evidence:
                        item["distance_evidence"] = {
                            **evidence,
                            "destination": destination or "Vị trí của bạn",
                            # Coordinates let the map draw the search radius around
                            # the place the customer actually named.
                            "destination_lat": target[0],
                            "destination_lng": target[1],
                            "travel_mode": travel_mode,
                            "provider": "Goong Distance Matrix",
                            "attribution": "Powered by Goong",
                        }
                valid = [item for item in valid if item.get("distance_evidence")]
                if max_km is not None:
                    valid = [item for item in valid if item["distance_evidence"]["distance_km"] <= max_km]
                if max_minutes is not None:
                    valid = [item for item in valid if item["distance_evidence"]["duration_minutes"] <= max_minutes]
                valid.sort(key=lambda item: item["distance_evidence"]["duration_minutes"])
                if not valid:
                    return GeoSearchResult(
                        [],
                        "Đã xác minh bằng Goong nhưng không có căn nào đạt "
                        "giới hạn quãng đường/thời gian đã yêu cầu.",
                        provider="Goong Maps API",
                        filtered=True,
                    )

            if categories and valid:
                nearby_results = await asyncio.gather(*[
                    self.nearby_places(
                        (float(item["latitude"]), float(item["longitude"])), categories
                    )
                    for item in valid[:5]
                ], return_exceptions=True)
                for item, nearby in zip(valid[:5], nearby_results, strict=False):
                    if isinstance(nearby, list):
                        item["nearby_evidence"] = nearby

                if not any(item.get("nearby_evidence") for item in valid):
                    return GeoSearchResult(
                        valid,
                        "Đã truy vấn Goong Places nhưng chưa tìm thấy tiện ích phù hợp "
                        "trong bán kính kiểm tra.",
                        provider="Goong Maps API",
                        filtered=max_km is not None or max_minutes is not None,
                    )

            return GeoSearchResult(
                valid,
                provider="Goong Maps API",
                filtered=max_km is not None or max_minutes is not None,
            )
        except (httpx.HTTPError, ValueError, KeyError):
            logger.exception("Geo provider request failed")
            return GeoSearchResult(
                properties,
                "Geo Service tạm thời không phản hồi; kết quả chưa được lọc theo khoảng cách.",
            )


_geo_service: GeoService | None = None


def get_geo_service() -> GeoService:
    global _geo_service
    if _geo_service is None:
        _geo_service = GeoService()
    return _geo_service
