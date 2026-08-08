"""Booking Agent - Tour request and appointment creation."""

import json
import logging
from datetime import datetime, timedelta
from typing import Optional

from src.agents.state import AgentState, AgentType
from src.agents.tools.booking_tools import (
    calculate_viewing_time,
    create_booking,
    propose_time_slots,
    get_booking_status,
    cancel_booking,
)
from src.agents.tools.property_tools import hold_property, release_hold
from src.config import get_settings

logger = logging.getLogger(__name__)


async def booking_agent(state: AgentState) -> dict:
    """Booking agent - handles tour requests and appointment creation.

    Args:
        state: Current agent state

    Returns:
        Updated state with booking information
    """
    intent = state.get("intent")
    entities = state.get("metadata", {}).get("entities", {})
    customer_id = state.get("customer_id")
    current_property_id = state.get("current_property_id")
    booking_id = state.get("booking_id")

    settings = get_settings()

    # Handle different booking intents
    if intent == "CANCEL_BOOKING":
        return await _handle_cancel(state)

    elif intent == "RESCHEDULE":
        return await _handle_reschedule(state)

    # Default: Create or update booking
    return await _handle_booking_flow(state)


async def _handle_cancel(state: AgentState) -> dict:
    """Handle booking cancellation.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    booking_id = state.get("booking_id")
    entities = state.get("metadata", {}).get("entities", {})
    booking_code = entities.get("booking_code")

    if not booking_id and not booking_code:
        return {
            "response": "Bạn muốn hủy booking nào? Vui lòng cung cấp mã booking hoặc tôi có thể liệt kê các booking của bạn.",
            "suggested_actions": ["Cung cấp mã booking", "Xem danh sách booking của tôi"],
        }

    try:
        # Get booking_id if only booking_code is provided
        if not booking_id and booking_code:
            # Would need to look up booking by code
            # For now, assume booking_id is set
            pass

        result_str = cancel_booking.invoke({
            "booking_id": booking_id or booking_code,
            "reason": "Customer requested cancellation",
        })
        result = json.loads(result_str)

        if "error" in result:
            return {
                "response": f"Không thể hủy booking: {result['error']}",
                "error": result["error"],
            }

        return {
            "response": f"✅ Đã hủy booking **{result.get('booking_code')}** thành công.\n\nChúng tôi rất tiếc khi bạn không thể đến. Bạn có thể đặt lịch xem nhà khác bất cứ lúc nào.",
            "booking_id": None,
            "analysis": "Booking cancelled",
        }

    except Exception as e:
        logger.error(f"Error cancelling booking: {e}")
        return {
            "response": f"Gặp lỗi khi hủy booking: {str(e)}",
            "error": str(e),
        }


async def _handle_reschedule(state: AgentState) -> dict:
    """Handle booking reschedule.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    # For now, redirect to booking flow with existing property
    return {
        "response": "Để dời lịch, tôi cần biết thời gian mới bạn muốn. Bạn muốn đặt lịch vào ngày nào và khung giờ nào?",
        "suggested_actions": ["Đề xuất lịch mới", "Hủy booking này"],
        "next_action": "reschedule",
    }


async def _handle_booking_flow(state: AgentState) -> dict:
    """Handle the main booking flow.

    Args:
        state: Current agent state

    Returns:
        Updated state with booking information
    """
    customer_id = state.get("customer_id")
    property_id = state.get("current_property_id")
    selected_slots = state.get("selected_slots", [])
    selected_slot_id = state.get("selected_slot_id")
    search_criteria = state.get("search_criteria", {})

    # Step 1: Check if we have property
    if not property_id:
        # Get property from entities or selected properties
        selected_props = state.get("selected_properties", [])
        if selected_props:
            property_id = selected_props[0].get("id")

        if not property_id:
            return {
                "response": "Bạn muốn đặt lịch xem căn nào? Vui lòng chọn một bất động sản trước.",
                "suggested_actions": ["Tìm bất động sản", "Chọn từ danh sách đã xem"],
                "current_agent": AgentType.INVENTORY,
            }

    # Step 2: Propose time slots if none selected
    if not selected_slots:
        return await _propose_slots(state, property_id)

    # Step 3: Create booking if slot is selected
    if selected_slot_id:
        return await _create_booking(state, selected_slot_id)

    # Still proposing slots
    return await _format_slot_proposal(state, selected_slots)


async def _propose_slots(state: AgentState, property_id: str) -> dict:
    """Propose available time slots for booking.

    Args:
        state: Current agent state
        property_id: Property UUID

    Returns:
        Updated state with proposed slots
    """
    customer_id = state.get("customer_id")
    entities = state.get("metadata", {}).get("entities", {})

    # Default to tomorrow at 10 AM
    preferred_date = entities.get("preferred_date")
    if not preferred_date:
        tomorrow = datetime.utcnow().date() + timedelta(days=1)
        preferred_date = tomorrow.strftime("%Y-%m-%d")

    try:
        result_str = propose_time_slots.invoke({
            "property_id": property_id,
            "customer_id": customer_id or "default",
            "preferred_date": preferred_date,
            "num_slots": 3,
        })
        result = json.loads(result_str)

        if "error" in result:
            return {
                "response": f"Không thể đề xuất lịch: {result['error']}",
                "error": result["error"],
            }

        slots = result.get("available_slots", [])
        return await _format_slot_proposal(state, slots)

    except Exception as e:
        logger.error(f"Error proposing slots: {e}")
        return {
            "response": f"Gặp lỗi khi đề xuất lịch: {str(e)}",
            "error": str(e),
        }


async def _format_slot_proposal(state: AgentState, slots: list) -> dict:
    """Format slot proposals for user.

    Args:
        state: Current agent state
        slots: List of proposed slots

    Returns:
        Updated state with formatted response
    """
    if not slots:
        return {
            "response": "Hiện tại không có khung giờ trống. Bạn có thể chọn ngày khác không?",
            "suggested_actions": ["Chọn ngày khác", "Để tôi kiểm tra lại sau"],
        }

    selected_props = state.get("selected_properties", [])
    property_title = selected_props[0].get("title") if selected_props else "căn hộ"

    response = f"Tôi đã tìm thấy các khung giờ trống để xem **{property_title}**:\n\n"

    for i, slot in enumerate(slots, 1):
        start = datetime.fromisoformat(slot["starts_at"])
        end = datetime.fromisoformat(slot["ends_at"])
        date_str = start.strftime("%A, %d/%m/%Y")
        time_str = start.strftime("%H:%M")
        end_time_str = end.strftime("%H:%M")
        sale_name = slot.get("sale_name", "Sale")

        response += f"**{i}. {date_str}**\n"
        response += f"   ⏰ {time_str} - {end_time_str}\n"
        response += f"   👤 Sale: {sale_name}\n"
        response += f"   ID: `{slot['slot_id']}`\n\n"

    response += "Bạn chọn khung giờ nào? (VD: 1, 2, hoặc 3)\n\n"
    response += "Nếu không phù hợp, tôi có thể đề xuất ngày khác."

    return {
        "selected_slots": slots,
        "response": response,
        "suggested_actions": ["Chọn khung giờ 1", "Chọn khung giờ 2", "Chọn khung giờ 3", "Chọn ngày khác"],
    }


async def _create_booking(state: AgentState, slot_id: str) -> dict:
    """Create booking from selected slot.

    Args:
        state: Current agent state
        slot_id: Selected slot UUID

    Returns:
        Updated state with booking confirmation
    """
    customer_id = state.get("customer_id")
    property_id = state.get("current_property_id")
    slots = state.get("selected_slots", [])

    # Find selected slot
    selected_slot = None
    for slot in slots:
        if slot.get("slot_id") == slot_id:
            selected_slot = slot
            break

    if not selected_slot:
        return {
            "response": "Khung giờ không hợp lệ. Vui lòng chọn lại.",
            "selected_slot_id": None,
        }

    try:
        # Hold the property first
        if customer_id:
            hold_result_str = hold_property.invoke({
                "property_id": property_id,
                "customer_id": customer_id,
                "hold_minutes": 15,
            })
            hold_result = json.loads(hold_result_str)
            if "error" in hold_result:
                logger.warning(f"Hold failed: {hold_result['error']}")
                # Continue anyway - booking can still be created

        # Create booking
        result_str = create_booking.invoke({
            "customer_id": customer_id or "default",
            "property_id": property_id,
            "sale_user_id": selected_slot.get("sale_id"),
            "starts_at": selected_slot.get("starts_at"),
            "ends_at": selected_slot.get("ends_at"),
            "party_size": 1,
        })
        result = json.loads(result_str)

        if "error" in result:
            return {
                "response": f"Không thể tạo booking: {result['error']}",
                "error": result["error"],
            }

        booking_id = result.get("booking_id")
        booking_code = result.get("booking_code")
        start = datetime.fromisoformat(result.get("starts_at", ""))
        date_str = start.strftime("%A, %d/%m/%Y")
        time_str = start.strftime("%H:%M")

        response = f"🎉 **Đặt lịch thành công!**\n\n"
        response += f"**Mã booking:** `{booking_code}`\n"
        response += f"**Ngày:** {date_str}\n"
        response += f"**Giờ:** {time_str}\n"
        response += f"**Sale:** {selected_slot.get('sale_name', 'Đã phân công')}\n\n"
        response += "Sale sẽ liên hệ với bạn để xác nhận trước buổi xem nhà.\n\n"
        response += "Bạn có cần thêm thông tin gì không?"

        return {
            "response": response,
            "booking_id": booking_id,
            "booking_code": booking_code,
            "selected_slots": [],
            "selected_slot_id": None,
            "analysis": f"Booking {booking_code} created successfully",
        }

    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        return {
            "response": f"Gặp lỗi khi tạo booking: {str(e)}",
            "error": str(e),
        }


async def check_booking_status(booking_id: str) -> dict:
    """Check booking status.

    Args:
        booking_id: Booking UUID

    Returns:
        Booking status information
    """
    try:
        result_str = get_booking_status.invoke({"booking_id": booking_id})
        result = json.loads(result_str)

        if "error" in result:
            return {"error": result["error"]}

        status_emoji = {
            "CONFIRMED": "✅",
            "IN_PROGRESS": "🔄",
            "COMPLETED": "🎉",
            "CANCELLED": "❌",
            "NO_SHOW": "👋",
        }
        emoji = status_emoji.get(result.get("status"), "📋")

        response = f"{emoji} **Trạng thái booking `{result.get('booking_code')}`:**\n\n"
        response += f"- Trạng thái: {result.get('status')}\n"

        if result.get("starts_at"):
            start = datetime.fromisoformat(result.get("starts_at"))
            response += f"- Ngày: {start.strftime('%A, %d/%m/%Y')}\n"
            response += f"- Giờ: {start.strftime('%H:%M')}\n"

        if result.get("property"):
            response += f"- Căn: {result['property'].get('title')}\n"

        if result.get("sale"):
            response += f"- Sale: {result['sale'].get('name')}\n"

        return {"response": response, "status_data": result}

    except Exception as e:
        logger.error(f"Error checking booking status: {e}")
        return {"error": str(e)}
