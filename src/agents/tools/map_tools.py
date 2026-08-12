"""Map-related tools for the agent.

Provides location services:
- Get map link for a property
- Geocoding (address to coordinates)
- Reverse geocoding (coordinates to address)
- Embed map URL for frontend display
"""

import json
import logging
from uuid import UUID

from langchain_core.tools import tool

from src.database.connection import get_session_context
from src.database.models import Project, Property

logger = logging.getLogger(__name__)


# ============== Map Provider URLs ==============

def _get_google_maps_link(lat: float, lng: float, zoom: int = 15) -> str:
    """Generate Google Maps link."""
    return f"https://www.google.com/maps?q={lat},{lng}&z={zoom}"


def _get_openstreetmap_embed(lat: float, lng: float, zoom: int = 15) -> str:
    """Generate OpenStreetMap embed URL (free, no API key needed)."""
    return (
        f"https://www.openstreetmap.org/export/embed.html?"
        f"bbox={lng-0.01},{lat-0.01},{lng+0.01},{lat+0.01}"
        f"&layer=mapnik&marker={lat},{lng}"
    )


def _get_google_maps_embed(lat: float, lng: float, zoom: int = 15) -> str:
    """Generate Google Maps embed URL."""
    return (
        f"https://www.google.com/maps/embed/v1/view?"
        f"key=YOUR_API_KEY&q={lat},{lng}&zoom={zoom}"
    )


def _get_leaflet_embed(lat: float, lng: float, title: str = "") -> str:
    """Generate Leaflet map embed HTML (for frontend)."""
    marker_title = title.replace("'", "\\'").replace('"', '\\"')
    return (
        f'<div class="property-map" data-lat="{lat}" data-lng="{lng}" data-title="{marker_title}">'
        f'<div class="map-placeholder">📍 {title}<br><small>{lat:.6f}, {lng:.6f}</small></div>'
        f'</div>'
    )


# ============== Geocoding (Vietnam) ==============

# Common Vietnamese province/district centers (fallback when no coordinates)
VIETNAM_LOCATIONS = {
    # Province -> center coordinates
    "hồ chí minh": (10.8231, 106.6297),
    "hà nội": (21.0285, 105.8542),
    "đà nẵng": (16.0544, 108.2022),
    "hải phòng": (20.8449, 106.6881),
    "cần thơ": (10.0452, 105.7469),
    "bình dương": (10.9804, 106.6517),
    "đồng nai": (10.9554, 106.8906),
    "bà rịa vũng tàu": (10.4806, 107.1824),
    "long an": (10.6928, 106.4617),
    "tiền giang": (10.4498, 106.3421),
    "an giang": (10.5214, 105.1219),
    "cà mau": (9.0531, 105.1472),
    "hậu giang": (9.7575, 105.6415),
    "kiên giang": (9.8249, 105.6532),
    "sóc trăng": (9.6027, 105.9742),
    "bạc liêu": (9.2941, 105.7268),
    "trà vinh": (9.9472, 106.3379),
    "vĩnh long": (10.0689, 105.9733),
    "bến tre": (10.2414, 106.6341),
    "quảng nam": (15.5734, 108.4735),
    "quảng ngãi": (15.1205, 108.7922),
    "bình định": (14.0865, 108.8387),
    "phú yên": (13.0888, 109.3016),
    "khánh hòa": (12.2560, 109.0535),
    "ninh thuận": (11.5644, 108.9894),
    "bình thuận": (10.9255, 108.0673),
    "thanh hóa": (19.9638, 105.2872),
    "nghệ an": (18.6654, 105.6890),
    "hà tĩnh": (18.3415, 105.6710),
    "quảng bình": (17.6228, 106.3477),
    "quảng trị": (16.7381, 107.0874),
    "thừa thiên huế": (16.4619, 107.5870),
    "hòa bình": (20.4866, 105.4180),
    "vĩnh phúc": (21.3061, 105.7548),
    "bắc ninh": (21.1205, 106.1135),
    "hưng yên": (20.6464, 106.0511),
    "hải dương": (20.9376, 106.3320),
    "nam định": (20.2544, 106.1651),
    "thái bình": (20.4497, 106.3368),
    "ninh bình": (20.1091, 105.9750),
    "hà nam": (20.3593, 105.9622),
    "phú thọ": (21.4097, 105.2279),
    "tuyên quang": (21.8176, 105.2242),
    "yên bái": (21.7254, 104.9110),
    "lào cai": (22.4802, 103.9758),
    "điện biên": (21.3833, 103.0382),
    "sơn la": (21.1145, 103.8936),
    "lai châu": (22.3833, 103.4704),
    "hà giang": (22.8251, 104.9828),
    "cao bằng": (22.6556, 106.2522),
    "bắc kạn": (22.1306, 105.8560),
    "thái nguyên": (21.5941, 105.8483),
    "lạng sơn": (21.8537, 106.7617),
    "quảng ninh": (20.9101, 107.1830),
    "bắc giang": (21.2761, 106.1946),
    "vũng tàu": (10.4806, 107.1824),
    "thủ đức": (10.8231, 106.6297),
}


def _estimate_coordinates(address: str, district: str = "", province: str = "") -> tuple[float, float] | None:
    """Estimate coordinates from address components.

    Uses known center points for Vietnamese provinces/districts as fallback.
    Handles both diacritics and ASCII versions of names.
    """
    import unicodedata

    def normalize(s: str) -> str:
        """Remove diacritics for matching."""
        return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii').lower()

    province_lower = province.lower().strip() if province else ""
    district_lower = district.lower().strip() if district else ""
    province_normalized = normalize(province_lower)
    district_normalized = normalize(district_lower)

    # Check if we have match for province (both original and normalized)
    for name, coords in VIETNAM_LOCATIONS.items():
        name_normalized = normalize(name)
        if name in province_lower or name_normalized in province_normalized or province_normalized in name_normalized:
            lat, lng = coords
            # Adjust slightly for district
            if district_lower or district_normalized:
                # Major districts get slight adjustments
                district_adjustments = {
                    "quan 1": (0.002, -0.003),
                    "quan 2": (0.005, 0.002),
                    "quan 3": (0.001, -0.002),
                    "quan 4": (-0.001, -0.001),
                    "quan 5": (-0.001, -0.003),
                    "quan 6": (-0.002, -0.004),
                    "quan 7": (0.003, 0.005),
                    "quan 8": (-0.003, -0.005),
                    "quan 9": (0.006, 0.003),
                    "quan 10": (-0.001, -0.003),
                    "quan 11": (-0.002, -0.003),
                    "quan 12": (-0.004, -0.006),
                    "thu duc": (0.005, 0.002),
                    "binh thanh": (0.002, -0.001),
                    "go vap": (-0.001, -0.002),
                    "phu nhuan": (0.000, -0.002),
                    "tan binh": (-0.002, -0.003),
                    "tan phu": (-0.003, -0.004),
                    "binh tan": (-0.004, -0.005),
                    "hoc mon": (-0.008, -0.008),
                    "cu chi": (-0.010, -0.012),
                    "nha be": (0.003, 0.008),
                    "cau giay": (0.003, 0.002),
                    "dong da": (-0.001, 0.000),
                    "hai ba trung": (-0.002, -0.001),
                    "thanh xuan": (-0.002, 0.002),
                    "hoang mai": (-0.003, 0.003),
                    "long bien": (-0.002, -0.003),
                    "tu liem": (0.003, 0.001),
                    "ba dinh": (0.000, -0.002),
                    "cam": (0.000, -0.002),
                    "hoan kiem": (0.000, -0.002),
                }
                for d_name, adj in district_adjustments.items():
                    if d_name in district_normalized:
                        lat += adj[0]
                        lng += adj[1]
                        break
            return (lat, lng)

    return None


# ============== Agent Tools ==============

@tool
async def get_property_location(
    property_id: str,
) -> str:
    """Lấy thông tin vị trí và link bản đồ của một bất động sản.

    Args:
        property_id: UUID của bất động sản

    Returns:
        Thông tin vị trí và link bản đồ (JSON)
    """
    async with get_session_context() as session:
        from sqlalchemy import select

        stmt = select(Property).where(Property.id == UUID(property_id))
        result = await session.execute(stmt)
        prop = result.scalar_one_or_none()

        if not prop:
            return json.dumps({"error": "Property not found"})

        # Check if property has coordinates
        if prop.latitude and prop.longitude:
            lat = float(prop.latitude)
            lng = float(prop.longitude)

            return json.dumps({
                "property_id": property_id,
                "title": prop.title,
                "has_coordinates": True,
                "latitude": lat,
                "longitude": lng,
                "address": prop.address_line or "",
                "district": prop.district or "",
                "province": prop.province or "",
                "google_maps_link": _get_google_maps_link(lat, lng),
                "openstreetmap_embed": _get_openstreetmap_embed(lat, lng),
                "leaflet_embed": _get_leaflet_embed(lat, lng, prop.title),
            }, ensure_ascii=False)

        # Try to get from project
        project_coords = None
        if prop.project_id:
            from sqlalchemy import select as sel
            proj_stmt = sel(Project).where(Project.id == prop.project_id)
            proj_result = await session.execute(proj_stmt)
            project = proj_result.scalar_one_or_none()
            if project and project.latitude and project.longitude:
                project_coords = (float(project.latitude), float(project.longitude))

        # Estimate coordinates
        coords = project_coords or _estimate_coordinates(
            address=prop.address_line or "",
            district=prop.district,
            province=prop.province,
        )

        if coords:
            lat, lng = coords
            return json.dumps({
                "property_id": property_id,
                "title": prop.title,
                "has_coordinates": True,
                "latitude": lat,
                "longitude": lng,
                "is_estimated": True,
                "address": prop.address_line or "",
                "district": prop.district or "",
                "province": prop.province or "",
                "google_maps_link": _get_google_maps_link(lat, lng, zoom=14),
                "openstreetmap_embed": _get_openstreetmap_embed(lat, lng, zoom=14),
                "leaflet_embed": _get_leaflet_embed(lat, lng, prop.title),
                "note": "Coordinates are estimated based on district/province",
            }, ensure_ascii=False)

        # No coordinates available
        return json.dumps({
            "property_id": property_id,
            "title": prop.title,
            "has_coordinates": False,
            "address": prop.address_line or "",
            "district": prop.district or "",
            "province": prop.province or "",
            "note": "Coordinates not available for this property",
        }, ensure_ascii=False)


@tool
def get_map_link_for_address(
    address: str,
    district: str | None = None,
    province: str | None = None,
) -> str:
    """Lấy link bản đồ cho một địa chỉ.

    Args:
        address: Địa chỉ đầy đủ hoặc một phần
        district: Quận/Huyện (tùy chọn)
        province: Tỉnh/Thành phố (tùy chọn)

    Returns:
        Link bản đồ và thông tin vị trí (JSON)
    """
    # Try to get coordinates
    coords = _estimate_coordinates(address, district or "", province or "")

    if coords:
        lat, lng = coords
        full_address = f"{address}, {district}, {province}".strip(", ")

        return json.dumps({
            "success": True,
            "has_coordinates": True,
            "latitude": lat,
            "longitude": lng,
            "is_estimated": True,
            "address": full_address,
            "google_maps_link": _get_google_maps_link(lat, lng, zoom=15),
            "openstreetmap_link": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=15/{lat}/{lng}",
            "leaflet_embed": _get_leaflet_embed(lat, lng, full_address),
            "note": "Coordinates are estimated. For exact location, please verify on map.",
        }, ensure_ascii=False)

    # No coordinates available - return search link
    search_query = f"{address}, {district}, {province}".strip(", ")
    return json.dumps({
        "success": True,
        "has_coordinates": False,
        "address": search_query,
        "google_maps_search": f"https://www.google.com/maps/search/?api=1&query={search_query.replace(' ', '+')}",
        "openstreetmap_search": f"https://www.openstreetmap.org/search?query={search_query.replace(' ', '+')}",
        "note": "Exact coordinates not available. Use search links to find on map.",
    }, ensure_ascii=False)


@tool
async def get_property_map_embed(
    property_id: str,
    map_provider: str = "leaflet",
) -> str:
    """Lấy embed HTML cho bản đồ property (để hiển thị trên frontend).

    Args:
        property_id: UUID của bất động sản
        map_provider: 'leaflet' (mặc định, free) hoặc 'google' (cần API key)

    Returns:
        Embed HTML hoặc link bản đồ (JSON)
    """
    async with get_session_context() as session:
        from sqlalchemy import select

        stmt = select(Property).where(Property.id == UUID(property_id))
        result = await session.execute(stmt)
        prop = result.scalar_one_or_none()

        if not prop:
            return json.dumps({"error": "Property not found"})

        # Determine coordinates
        if prop.latitude and prop.longitude:
            lat, lng = float(prop.latitude), float(prop.longitude)
            is_estimated = False
        else:
            coords = _estimate_coordinates(
                prop.address_line or "", prop.district, prop.province
            )
            if coords:
                lat, lng = coords
                is_estimated = True
            else:
                return json.dumps({
                    "error": "No coordinates available",
                    "property_id": property_id,
                    "title": prop.title,
                })

        title = prop.title
        address = f"{prop.ward or ''}, {prop.district or ''}, {prop.province or ''}".strip(", ")

        if map_provider == "leaflet":
            return json.dumps({
                "success": True,
                "map_provider": "leaflet",
                "latitude": lat,
                "longitude": lng,
                "zoom": 15,
                "title": title,
                "address": address,
                "embed_html": _get_leaflet_embed(lat, lng, title),
                "marker_data": {
                    "lat": lat,
                    "lng": lng,
                    "title": title,
                    "address": address,
                    "property_id": str(prop.id),
                },
                "is_estimated": is_estimated,
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "success": True,
                "map_provider": "google",
                "latitude": lat,
                "longitude": lng,
                "zoom": 15,
                "title": title,
                "address": address,
                "embed_url": _get_google_maps_embed(lat, lng, 15),
                "direct_link": _get_google_maps_link(lat, lng),
                "is_estimated": is_estimated,
            }, ensure_ascii=False)


# Export all tools
__all__ = [
    "get_property_location",
    "get_map_link_for_address",
    "get_property_map_embed",
]
