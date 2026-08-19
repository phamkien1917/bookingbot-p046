"""Inventory Agent - Property search and information."""

import json
import logging
from typing import Any

from src.agents.state import AgentState, AgentType
from src.agents.tools.property_tools import (
    search_properties,
    check_property_availability,
)
from src.services.memory import get_long_term_memory

logger = logging.getLogger(__name__)


async def inventory_agent(state: AgentState) -> dict:
    """Inventory agent - searches properties and provides information.

    Args:
        state: Current agent state

    Returns:
        Updated state with search results
    """
    intent = state.get("intent")
    entities = state.get("metadata", {}).get("entities", {})
    search_criteria = state.get("search_criteria")

    # Merge deterministic search criteria with LLM entities
    search_criteria = state.get("search_criteria") or {}
    
    # Fallbacks from LLM entities if deterministic parsing missed them
    district = search_criteria.get("district") or entities.get("district")
    province = search_criteria.get("province") or entities.get("province")
    property_kind = search_criteria.get("property_kind") or entities.get("property_kind")
    
    # Prices from deterministic parsing take precedence. If none, try LLM entities.
    min_price = search_criteria.get("min_price")
    max_price = search_criteria.get("max_price")
    keyword = search_criteria.get("keyword") or entities.get("keyword")
    
    if min_price is None and max_price is None:
        budget = entities.get("budget", {})
        if isinstance(budget, dict):
            min_price = budget.get("min")
            max_price = budget.get("max")
        else:
            max_price = budget

    min_bedrooms = search_criteria.get("min_bedrooms") or entities.get("bedrooms")

    search_criteria = {
        "keyword": keyword,
        "district": district if district and province and district.lower() not in province.lower() else (district if district and not province else None),
        "province": province,
        "property_kind": property_kind,
        "min_price": min_price,
        "max_price": max_price,
        "min_bedrooms": min_bedrooms,
    }

    # If user wants to search but provides no criteria, ask them
    has_criteria = any([
        keyword, district, province, property_kind, min_price, max_price, min_bedrooms
    ])
    
    if intent == "SEARCH_PROPERTY" and not has_criteria:
        return {
            "response": "Bạn đang tìm nhà ở khu vực nào, mức giá khoảng bao nhiêu, và loại bất động sản nào (căn hộ, nhà phố...)?",
            "selected_properties": [],
            "suggested_actions": [
                "Tìm căn hộ dưới 3 tỷ",
                "Tìm nhà phố quận 7",
                "Tìm biệt thự ven sông"
            ]
        }

    # Get customer preferences from long-term memory
    customer_id = state.get("customer_id")
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

    # Search properties
    search_results = None
    try:
        result_str = await search_properties.ainvoke({
            "keyword": search_criteria.get("keyword"),
            "district": search_criteria.get("district"),
            "province": search_criteria.get("province"),
            "property_kind": search_criteria.get("property_kind"),
            "min_price": search_criteria.get("min_price"),
            "max_price": search_criteria.get("max_price"),
            "min_bedrooms": search_criteria.get("min_bedrooms"),
            "limit": 10,
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
    updates = {
        "selected_properties": search_results,
        "search_criteria": search_criteria,
        "analysis": f"Found {len(search_results)} properties matching criteria",
    }

    # Generate response message
    if intent == "SEARCH_PROPERTY":
        response = "Dưới đây là một số bất động sản phù hợp với yêu cầu của bạn:"

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
            response = f"Thông tin về **{prop.get('title')}**:\n\n"
            response += f"- Mã căn: {prop.get('code')}\n"
            response += f"- Loại: {prop.get('property_kind')}\n"
            response += f"- Địa chỉ: {prop.get('district')}, {prop.get('province')}\n"
            response += f"- Diện tích: {prop.get('area_sqm')} m²\n"
            if prop.get("bedrooms"):
                response += f"- Phòng ngủ: {prop['bedrooms']}\n"
            if prop.get("bathrooms"):
                response += f"- Phòng tắm: {prop['bathrooms']}\n"
            price = prop.get("list_price")
            if price:
                price_str = f"{price/1e9:.1f} tỷ" if price >= 1e9 else f"{price/1e6:.0f} triệu"
                response += f"- Giá: {price_str}\n"

            updates["response"] = response
            updates["current_property_id"] = prop.get("id")
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
        availability_str = check_property_availability.invoke({
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
