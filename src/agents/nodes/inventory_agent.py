"""Inventory Agent - Property search and information."""

import json
import logging
from typing import Any

from src.agents.state import AgentState, AgentType
from src.agents.tools.property_tools import (
    search_properties,
    check_property_availability,
)
from src.agents.tools.map_tools import get_property_location
from src.services.memory import get_long_term_memory
from src.services.redis_service import get_distributed_lock, get_property_cache

logger = logging.getLogger(__name__)


async def inventory_agent(state: AgentState) -> dict:
    """Inventory agent - searches properties and provides information.

    Uses distributed lock to prevent duplicate processing when multiple
    agents are querying the same property simultaneously.

    Args:
        state: Current agent state

    Returns:
        Updated state with search results
    """
    intent = state.get("intent")
    entities = state.get("metadata", {}).get("entities", {})
    search_criteria = state.get("search_criteria")
    session_id = state.get("session_id")
    customer_id = state.get("customer_id")

    # === Distributed Lock: Prevent duplicate property processing ===
    # Use lock to ensure same property isn't being processed by multiple agents
    lock = get_distributed_lock()
    property_id = entities.get("property_id")
    lock_token = None

    if property_id:
        lock_key = f"inventory:{property_id}"
        lock_token = await lock.acquire(lock_key, ttl=30, blocking=True)
        if not lock_token:
            logger.warning(f"Could not acquire lock for property {property_id}, processing anyway")
            lock_token = None  # Allow processing even without lock

    try:
        return await _inventory_agent_impl(
            state, intent, entities, search_criteria, session_id, customer_id
        )
    finally:
        # Release lock if acquired
        if lock_token and property_id:
            await lock.release(f"inventory:{property_id}", lock_token)


async def _inventory_agent_impl(
    state: AgentState,
    intent: str,
    entities: dict,
    search_criteria: dict,
    session_id: str,
    customer_id: str,
) -> dict:
    """Implementation of inventory agent logic (separated for lock handling)."""
    # === GUARD: GET_INFO yêu cầu customer đăng nhập ===
    # Ngăn chặn IDOR + enumeration bởi anonymous users.
    if intent == "GET_INFO" and not customer_id:
        return {
            "response": (
                "Vui lòng đăng nhập để xem chi tiết căn hộ cụ thể. "
                "Tôi có thể giúp bạn tìm kiếm các căn hộ phù hợp mà không cần đăng nhập."
            ),
            "suggested_actions": ["Đăng nhập", "Tìm căn hộ theo tiêu chí"],
            "current_property_id": None,
        }

    # === GUARD: GET_INFO cần property_id hoặc keyword cụ thể ===
    if intent == "GET_INFO" and not entities.get("property_id") and not search_criteria.get("keyword"):
        return {
            "response": (
                "Bạn muốn hỏi về căn nào? Vui lòng cung cấp mã căn hoặc "
                "chọn một căn từ kết quả tìm kiếm trước đó."
            ),
            "suggested_actions": ["Cung cấp mã căn", "Xem danh sách đã tìm"],
            "current_property_id": None,
        }

    # === Extract search criteria ===
    # Lưu ý: KHÔNG hard-code province mặc định nữa — nếu thiếu thì search
    # sẽ rộng hơn nhưng an toàn hơn (trước đây bị ép về HCM).
    if not search_criteria:
        search_criteria = {
            "district": entities.get("district"),
            "province": entities.get("province"),
            "keyword": entities.get("keyword"),
            "property_kind": entities.get("property_kind"),
            "min_price": entities.get("budget", {}).get("min") if isinstance(entities.get("budget"), dict) else None,
            "max_price": entities.get("budget", {}).get("max") if isinstance(entities.get("budget"), dict) else entities.get("budget"),
            "min_bedrooms": entities.get("bedrooms"),
            "min_bathrooms": entities.get("bathrooms"),
            "min_area": entities.get("area_sqm"),
        }

    # === Reset current_property_id khi search mới ===
    # Tránh state pollution từ task trước.
    updates: dict = {"current_property_id": None}

    # Get customer preferences from long-term memory
    preferred_districts = []
    if customer_id:
        memory = get_long_term_memory()
        try:
            preferences = await memory.get_preferences(customer_id)
            # Filter for district preferences
            preferred_districts = [
                p["value"] for p in preferences
                if p["key"].startswith("district_") and p["value"]
            ]
        except Exception as e:
            logger.warning(f"Error getting preferences: {e}")

    # Search properties using tool's ainvoke (async)
    search_results = None
    try:
        result_str = await search_properties.ainvoke({
            "district": search_criteria.get("district"),
            "province": search_criteria.get("province"),
            "keyword": search_criteria.get("keyword"),
            "property_kind": search_criteria.get("property_kind"),
            "min_price": search_criteria.get("min_price"),
            "max_price": search_criteria.get("max_price"),
            "min_bedrooms": search_criteria.get("min_bedrooms"),
            "min_bathrooms": search_criteria.get("min_bathrooms"),
            "min_area": search_criteria.get("min_area"),
            "limit": 10,
            "session_id": session_id,
        })
        search_results = json.loads(result_str)
    except Exception as e:
        logger.error(f"Error searching properties: {e}")
        return {
            "response": f"Xin lỗi, tôi gặp lỗi khi tìm kiếm: {str(e)}",
            "error": str(e),
        }

    # Format response
    if "error" in search_results:
        return {
            "response": f"Xin lỗi, tôi gặp lỗi: {search_results['error']}",
            "error": search_results["error"],
        }

    if not search_results:
        return {
            "response": "Rất tiếc, hiện tại không có bất động sản nào phù hợp với tiêu chí của bạn. Bạn có muốn thay đổi điều kiện tìm kiếm không?",
            "selected_properties": [],
            "analysis": "No properties found matching criteria",
        }

    # Store results in state
    updates["selected_properties"] = search_results
    updates["search_criteria"] = search_criteria
    updates["analysis"] = f"Found {len(search_results)} properties matching criteria"

    # Generate response message
    if intent == "SEARCH_PROPERTY":
        response = "Tôi đã tìm được các bất động sản phù hợp cho bạn:\n\n"

        for i, prop in enumerate(search_results[:5], 1):  # Show top 5
            price = prop.get("list_price")
            if price:
                price_str = f"{price/1e9:.1f} tỷ" if price >= 1e9 else f"{price/1e6:.0f} triệu"
            else:
                price_str = "Liên hệ"

            response += f"**{i}. {prop.get('title', 'N/A')}**\n"
            response += f"   - Loại: {prop.get('property_kind', 'N/A')}\n"
            response += f"   - Khu vực: {prop.get('district', 'N/A')}\n"
            response += f"   - Diện tích: {prop.get('area_sqm', 'N/A')} m²\n"
            if prop.get("bedrooms"):
                response += f"   - Phòng ngủ: {prop['bedrooms']}\n"
            if prop.get("bathrooms"):
                response += f"   - Phòng tắm: {prop['bathrooms']}\n"
            response += f"   - Giá: {price_str}\n\n"

        response += "Bạn quan tâm căn nào? Tôi có thể giữ căn và đề xuất lịch xem cho bạn."

        updates["response"] = response
        updates["suggested_actions"] = [
            "Chọn một căn để xem chi tiết",
            "Yêu cầu xem thêm bất động sản khác",
            "Đặt lịch xem nhà",
        ]

    elif intent == "GET_INFO":
        # User asking about specific property or general info
        prop = search_results[0] if search_results else None
        if prop:
            # Get internal property ID for map lookup
            internal_id = prop.get("_internal_id")

            # Build response
            response = f"Thông tin về **{prop.get('title')}**:\n\n"
            response += f"- Loại: {prop.get('property_kind')}\n"
            ward = prop.get("ward") or ""
            district = prop.get("district") or ""
            province = prop.get("province") or ""
            address = ", ".join(filter(None, [ward, district, province]))
            response += f"- Khu vực: {address or 'Đang cập nhật'}\n"
            response += f"- Diện tích: {prop.get('area_sqm')} m²\n"
            if prop.get("bedrooms"):
                response += f"- Phòng ngủ: {prop['bedrooms']}\n"
            if prop.get("bathrooms"):
                response += f"- Phòng tắm: {prop['bathrooms']}\n"
            price = prop.get("list_price")
            if price:
                price_str = f"{price/1e9:.1f} tỷ" if price >= 1e9 else f"{price/1e6:.0f} triệu"
                response += f"- Giá: {price_str}\n"

            # Get map/location info if we have internal ID
            map_data = None
            if internal_id:
                try:
                    location_str = await get_property_location.ainvoke({"property_id": internal_id})
                    map_data = json.loads(location_str)
                    if map_data.get("has_coordinates"):
                        response += f"\n📍 [Xem vị trí trên bản đồ](https://www.google.com/maps?q={map_data['latitude']},{map_data['longitude']})\n"
                except Exception as e:
                    logger.warning(f"Could not get location for property: {e}")

            # Add map data to response for frontend (invisible marker)
            if map_data and map_data.get("has_coordinates"):
                response += f"\n<!-- MAP_DATA:{json.dumps(map_data)} -->\n"

            updates["response"] = response
            updates["map_data"] = map_data
        else:
            updates["response"] = "Xin lỗi, tôi không tìm thấy thông tin bạn yêu cầu."

    else:
        # Generic response
        updates["response"] = f"Tôi đã tìm thấy {len(search_results)} bất động sản phù hợp. Bạn muốn tìm hiểu thêm về căn nào?"

    return updates


async def get_property_details(property_id: str) -> dict:
    """Get detailed information about a property.

    Args:
        property_id: Property UUID

    Returns:
        Property details
    """
    try:
        # Check availability
        availability_str = await check_property_availability.ainvoke({
            "property_id": property_id,
        })
        availability = json.loads(availability_str)

        return {
            "availability": availability,
            "can_book": availability.get("can_book", False),
        }
    except Exception as e:
        logger.error(f"Error getting property details: {e}")
        return {"error": str(e)}
