"""Booking & Scheduling Agent for LangGraph.

Handles availability checking, slot selection, auth gating, booking creation,
cancellation with confirmation, and atomic rescheduling.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import or_, select

from src.agents.state import AgentState, AgentType, Intent
from src.database.connection import get_session_context
from src.database.models import Appointment, Property, TourRequest, UserRole
from src.exceptions import BookingConflictError, BookingNotFoundError
from src.schemas.booking import TourRequestCreate
from src.services.booking_service import (
    cancel_customer_booking,
    create_tour_request,
    get_customer_booking,
    get_my_tour_requests,
    list_available_slots,
    reschedule_customer_booking,
)
from src.services.chat_state_service import LOCAL_TZ
from src.utils.property_text import clean_property_title, match_property_by_title

logger = logging.getLogger(__name__)


def _format_slots_markdown(slots: list[dict[str, Any]], property_title: str, target_date: date) -> str:
    weekday_names = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật")
    lines = [
        f"Các khung giờ còn trống để xem **{property_title}** vào "
        f"**{weekday_names[target_date.weekday()]}, {target_date.strftime('%d/%m/%Y')}**:\n"
    ]
    for index, slot in enumerate(slots, 1):
        start = datetime.fromisoformat(slot["starts_at"])
        end = datetime.fromisoformat(slot["ends_at"])
        lines.append(
            f"**{index}. ⏰ {start.strftime('%H:%M')} – {end.strftime('%H:%M')}** · Sale phụ trách: *{slot['sale_name']}*"
        )
    lines.append("\nBạn chọn khung giờ số mấy?")
    return "\n".join(lines)


async def _find_tour_request_id(customer_id: UUID, code: str | None, active_id: str | None) -> UUID | None:
    async with get_session_context() as session:
        if code:
            stmt = (
                select(TourRequest.id)
                .outerjoin(Appointment, Appointment.tour_request_id == TourRequest.id)
                .where(
                    TourRequest.customer_user_id == customer_id,
                    or_(TourRequest.request_code == code, Appointment.booking_code == code),
                )
            )
            found = await session.scalar(stmt)
            if found:
                return found
        if active_id:
            try:
                return UUID(str(active_id))
            except (TypeError, ValueError):
                return None
    return None


async def booking_agent(state: AgentState) -> dict[str, Any]:
    """Booking Agent node: manages entire booking lifecycle."""
    intent = state.get("intent")
    customer_id_str = state.get("customer_id")
    customer_id = UUID(customer_id_str) if customer_id_str else None
    customer_role = state.get("customer_role")
    is_authenticated = customer_id is not None and customer_role == UserRole.CUSTOMER
    active_code = state.get("active_request_code")

    # Resume booking after login if user is in AWAITING_AUTH and says confirm/continue
    if state.get("phase") == "AWAITING_AUTH" and is_authenticated and intent in (Intent.CONFIRM, Intent.BOOK_APPOINTMENT, Intent.SELECT_SLOT):
        slot_idx = state.get("selected_slot_index")
        if isinstance(slot_idx, int):
            intent = Intent.SELECT_SLOT

    # ==========================================
    # 1. CANCEL BOOKING & CONFIRMATION FLOW
    # ==========================================
    if intent == Intent.CANCEL_BOOKING or state.get("phase") == "AWAITING_CANCEL_CONFIRMATION":
        if not is_authenticated:
            return {
                "response": "Bạn cần **đăng nhập tài khoản khách hàng** để quản lý hoặc hủy lịch xem nhà của mình.",
                "auth_required": True,
                "current_agent": AgentType.RESPOND,
            }

        # Step A: In confirmation phase
        if state.get("phase") == "AWAITING_CANCEL_CONFIRMATION":
            if intent == Intent.DENY:
                return {
                    "phase": "IDLE",
                    "pending_action": None,
                    "response": "Đã giữ nguyên lịch hẹn của bạn. Bạn cần hỗ trợ thêm thông tin gì khác không?",
                    "current_agent": AgentType.RESPOND,
                    "suggested_actions": ["Kiểm tra lại lịch", "Tìm thêm bất động sản"],
                }
            if intent in (Intent.CONFIRM, Intent.CANCEL_BOOKING):
                request_id = await _find_tour_request_id(customer_id, active_code, state.get("active_request_id"))
                if not request_id:
                    return {
                        "phase": "IDLE",
                        "response": "Không tìm thấy yêu cầu đặt lịch cần hủy.",
                        "current_agent": AgentType.RESPOND,
                    }
                async with get_session_context() as session:
                    booking = await cancel_customer_booking(session, request_id, customer_id, "Khách hàng yêu cầu qua Chatbot AI")
                return {
                    "phase": "IDLE",
                    "pending_action": None,
                    "response": f"✅ Đã hủy lịch xem nhà **{booking.request_code}** thành công. Chuyên viên Sale đã nhận được thông báo hủy.",
                    "current_agent": AgentType.RESPOND,
                    "suggested_actions": ["Tìm căn khác", "Đặt lịch mới"],
                }
            return {
                "response": "Vui lòng trả lời **xác nhận** để hủy lịch, hoặc **không** để tiếp tục giữ lịch hẹn.",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Xác nhận hủy", "Không, giữ lịch"],
            }

        # Step B: Trigger cancel
        request_id = await _find_tour_request_id(customer_id, active_code, state.get("active_request_id"))
        if not request_id:
            return {
                "response": "Bạn muốn hủy lịch hẹn nào? Vui lòng cung cấp mã yêu cầu (ví dụ: `TR-XXXXX` hoặc `BK-XXXXX`).",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Kiểm tra lịch của tôi"],
            }
        return {
            "phase": "AWAITING_CANCEL_CONFIRMATION",
            "active_request_id": str(request_id),
            "response": "Bạn có chắc chắn muốn hủy yêu cầu đặt lịch này không? Hãy trả lời **xác nhận** hoặc **không**.",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": ["Xác nhận", "Không"],
        }

    # ==========================================
    # 2. CHECK BOOKING STATUS
    # ==========================================
    if intent == Intent.CHECK_STATUS:
        if not is_authenticated:
            return {
                "response": "Bạn cần **đăng nhập** để kiểm tra danh sách và trạng thái lịch hẹn của mình.",
                "auth_required": True,
                "current_agent": AgentType.RESPOND,
            }

        request_id = await _find_tour_request_id(customer_id, active_code, state.get("active_request_id"))
        async with get_session_context() as session:
            if not request_id:
                bookings = await get_my_tour_requests(session, customer_id)
                if not bookings:
                    return {
                        "response": "Bạn hiện chưa có yêu cầu đặt lịch xem nhà nào. Hãy cùng mình tìm một căn phù hợp trước nhé!",
                        "current_agent": AgentType.RESPOND,
                        "suggested_actions": ["Tìm căn hộ Quận 7", "Tìm nhà phố Hà Nội"],
                    }
                lines = ["📋 **Danh sách các lịch xem nhà gần đây của bạn:**\n"]
                for b in bookings[:5]:
                    prop_title = clean_property_title(b.property.title) if b.property else "Bất động sản"
                    when = b.preferred_start.astimezone(LOCAL_TZ).strftime("%H:%M ngày %d/%m/%Y")
                    code = b.appointment.booking_code if b.appointment else b.request_code
                    lines.append(f"- **{code}** | {prop_title} | ⏰ {when} | Trạng thái: **{b.status}**")
                lines.append("\nBạn có thể nhắn mã để mình kiểm tra chi tiết, dời ngày hoặc hủy lịch.")
                return {
                    "response": "\n".join(lines),
                    "current_agent": AgentType.RESPOND,
                    "suggested_actions": [f"Xem {bookings[0].request_code}", "Đặt lịch mới"],
                }

            booking = await get_customer_booking(session, request_id, customer_id)
            prop = booking.property
            prop_title = clean_property_title(prop.title) if prop else "Bất động sản"
            prop_addr = prop.address if prop and hasattr(prop, "address") and prop.address else "Địa chỉ căn hộ"
            prop_id_val = str(prop.id) if prop and hasattr(prop, "id") else str(booking.id)
            local_start = booking.preferred_start.astimezone(LOCAL_TZ)
            local_end = booking.preferred_end.astimezone(LOCAL_TZ) if booking.preferred_end else local_start + timedelta(hours=1)
            duration_mins = int((local_end - local_start).total_seconds() / 60)
            apt = booking.appointment
            sale = booking.sale

            if apt and apt.status == "CONFIRMED":
                response_text = (
                    f"🎉 **Lịch xem nhà của bạn ĐÃ ĐƯỢC XÁC NHẬN!**\n\n"
                    f"📋 **Mã booking chính thức:** `{apt.booking_code}` (Yêu cầu: `{booking.request_code}`)\n\n"
                    f"🏠 **Căn hộ:**\n"
                    f"   - **Tên căn:** {prop_title}\n"
                    f"   - **Địa chỉ:** {prop_addr}\n"
                    f"   - **ID:** `{prop_id_val}`\n\n"
                    f"📅 **Lịch xem:**\n"
                    f"   - **Ngày:** {local_start.strftime('%d/%m/%Y')}\n"
                    f"   - **Giờ:** {local_start.strftime('%H:%M')} – {local_end.strftime('%H:%M')}\n"
                    f"   - **Thời lượng:** {duration_mins} phút\n\n"
                    f"👤 **Sale phụ trách:** {sale.full_name if sale else 'Chuyên viên tư vấn'}\n"
                    f"📍 **Địa điểm gặp:** {prop_addr}\n"
                    f"🔄 **Trạng thái:** `CONFIRMED` (Đã duyệt)\n\n"
                    f"💡 **Lưu ý:**\n"
                    f"   - Quý khách vui lòng mang theo CMND/CCCD\n"
                    f"   - Đến đúng giờ hẹn để trải nghiệm xem nhà trọn vẹn\n"
                    f"   - Liên hệ Sale hoặc nhắn trực tiếp cho Nera nếu cần dời lịch hoặc hủy\n\n"
                    f"Bạn nhớ đến đúng giờ nhé! 😊"
                )
            else:
                response_text = (
                    f"📋 **Thông tin trạng thái yêu cầu xem nhà:**\n\n"
                    f"- **Mã yêu cầu:** `{booking.request_code}`\n"
                    f"- **Bất động sản:** {prop_title}\n"
                    f"- **Địa chỉ:** {prop_addr}\n"
                    f"- **Thời gian:** {local_start.strftime('%H:%M ngày %d/%m/%Y')}\n"
                    f"- **Sale phụ trách:** {sale.full_name if sale else 'Đang phân công'}\n"
                    f"- **Trạng thái:** **{booking.status}**"
                )

            return {
                "active_request_id": str(booking.id),
                "active_request_code": booking.request_code,
                "response": response_text,
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Dời lịch sang ngày khác", "Hủy lịch này", "Tìm căn khác"],
            }

    # ==========================================
    # 3. RESCHEDULE BOOKING
    # ==========================================
    if intent == Intent.RESCHEDULE:
        if not is_authenticated:
            return {
                "response": "Bạn cần **đăng nhập** để dời lịch hẹn của mình.",
                "auth_required": True,
                "current_agent": AgentType.RESPOND,
            }

        request_id = await _find_tour_request_id(customer_id, active_code, state.get("active_request_id"))
        if not request_id:
            return {
                "response": "Bạn muốn dời lịch hẹn nào? Vui lòng gửi kèm mã `TR-XXXXX` hoặc `BK-XXXXX`.",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Kiểm tra lịch của tôi"],
            }

        async with get_session_context() as session:
            booking = await get_customer_booking(session, request_id, customer_id)
            property_id = booking.property_id
            prop_title = clean_property_title(booking.property.title) if booking.property else "căn nhà"

        target_date_str = state.get("requested_date")
        if not target_date_str:
            return {
                "active_request_id": str(request_id),
                "current_property_id": str(property_id),
                "pending_action": f"RESCHEDULE:{request_id}",
                "phase": "AWAITING_DATE",
                "response": f"Bạn muốn chuyển lịch xem **{prop_title}** sang ngày nào? (Ví dụ: 'ngày mai', 'thứ Bảy tuần này'...).",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Ngày mai", "Thứ Bảy tuần này", "Chủ Nhật tuần này"],
            }

        target_date = date.fromisoformat(target_date_str)
        async with get_session_context() as session:
            avail = await list_available_slots(session, property_id, target_date)
            slots = avail.get("slots", [])

        if not slots:
            return {
                "active_request_id": str(request_id),
                "current_property_id": str(property_id),
                "pending_action": f"RESCHEDULE:{request_id}",
                "phase": "AWAITING_DATE",
                "response": f"Ngày {target_date.strftime('%d/%m/%Y')} hiện chưa có khung giờ trống cho căn này. Bạn vui lòng chọn một ngày khác nhé.",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Chọn ngày khác"],
            }

        slot_actions = [f"Chọn khung giờ {i}" for i in range(1, len(slots) + 1)]
        return {
            "active_request_id": str(request_id),
            "current_property_id": str(property_id),
            "pending_action": f"RESCHEDULE:{request_id}",
            "phase": "AWAITING_SLOT",
            "selected_slots": slots,
            "response": _format_slots_markdown(slots, prop_title, target_date),
            "current_agent": AgentType.RESPOND,
            "suggested_actions": slot_actions,
        }

    # ==========================================
    # 4. SELECT SLOT -> COMPLETE BOOKING / RESCHEDULE
    # ==========================================
    if intent == Intent.SELECT_SLOT or state.get("phase") == "AWAITING_SLOT":
        slots = state.get("selected_slots", [])
        slot_idx = state.get("selected_slot_index")

        if slot_idx is None or slot_idx < 0 or slot_idx >= len(slots):
            return {
                "response": f"Danh sách hiện có {len(slots)} khung giờ. Bạn vui lòng chọn từ 1 đến {len(slots)} nhé.",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [f"Chọn khung giờ {i}" for i in range(1, min(len(slots) + 1, 5))],
            }

        # Auth Gate for guests
        if not is_authenticated:
            return {
                "phase": "AWAITING_AUTH",
                "auth_required": True,
                "selected_slot_index": slot_idx,
                "response": (
                    "Mình đã ghi nhận khung giờ bạn chọn! 🔒 Để gửi yêu cầu và nhận xác nhận từ Sale, "
                    "bạn vui lòng **đăng nhập tài khoản khách hàng** nhé. Sau khi đăng nhập, bạn chỉ cần nhắn 'tiếp tục'."
                ),
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Đăng nhập ngay"],
            }

        prop_id_str = state.get("current_property_id")
        if not prop_id_str:
            return {
                "phase": "IDLE",
                "response": "Không xác định được căn bạn muốn đặt lịch. Vui lòng chọn lại căn trong danh sách.",
                "current_agent": AgentType.RESPOND,
            }

        slot = slots[slot_idx]
        start = datetime.fromisoformat(slot["starts_at"])
        end = datetime.fromisoformat(slot["ends_at"])
        action = state.get("pending_action") or "CREATE_BOOKING"

        try:
            async with get_session_context() as session:
                if action.startswith("RESCHEDULE:"):
                    req_id = UUID(action.split(":", 1)[1])
                    booking = await reschedule_customer_booking(
                        session, req_id, customer_id, UUID(slot["sale_user_id"]), start, end
                    )
                    verb = "dời lịch hẹn"
                else:
                    conv_id = None
                    sess_id_str = state.get("session_id")
                    if sess_id_str:
                        try:
                            conv_id = UUID(sess_id_str)
                        except ValueError:
                            conv_id = None

                    new_req = await create_tour_request(
                        session,
                        customer_id,
                        TourRequestCreate(
                            property_id=UUID(prop_id_str),
                            sale_user_id=UUID(slot["sale_user_id"]),
                            preferred_start=start,
                            preferred_end=end,
                            pax_count=1,
                        ),
                        conversation_id=conv_id,
                    )
                    booking = await get_customer_booking(session, new_req.id, customer_id)
                    verb = "gửi yêu cầu đặt lịch"

            local_start = booking.preferred_start.astimezone(LOCAL_TZ)
            local_end = booking.preferred_end.astimezone(LOCAL_TZ) if booking.preferred_end else local_start + timedelta(hours=1)
            duration_mins = int((local_end - local_start).total_seconds() / 60)

            prop = booking.property
            prop_title = clean_property_title(prop.title) if prop else "Bất động sản"
            prop_addr = prop.address if prop and hasattr(prop, "address") and prop.address else "Địa chỉ căn hộ"
            prop_id_val = str(prop.id) if prop and hasattr(prop, "id") else prop_id_str
            sale_name = slot.get("sale_name") or "Chuyên viên tư vấn"

            enhanced_response = (
                f"🎉 **Đã {verb} thành công!**\n\n"
                f"📋 **Mã yêu cầu:** `{booking.request_code}`\n\n"
                f"🏠 **Căn hộ đã chọn:**\n"
                f"   - **Tên căn:** {prop_title}\n"
                f"   - **Địa chỉ:** {prop_addr}\n"
                f"   - **ID:** `{prop_id_val}`\n\n"
                f"📅 **Lịch xem nhà:**\n"
                f"   - **Ngày:** {local_start.strftime('%d/%m/%Y')}\n"
                f"   - **Giờ:** {local_start.strftime('%H:%M')} – {local_end.strftime('%H:%M')}\n"
                f"   - **Thời lượng:** {duration_mins} phút\n\n"
                f"👤 **Sale phụ trách:** {sale_name}\n"
                f"📍 **Địa điểm gặp:** {prop_addr}\n"
                f"🔄 **Trạng thái:** `WAITING_APPROVAL` (Đang chờ Sale xác nhận)\n\n"
                f"💡 **Lưu ý:**\n"
                f"   - Quý khách vui lòng mang theo CMND/CCCD\n"
                f"   - Đến đúng giờ hẹn để trải nghiệm xem nhà tốt nhất\n"
                f"   - Liên hệ Sale hoặc nhắn trực tiếp cho Nera nếu cần đổi ngày/hủy lịch\n\n"
                f"Bạn nhớ đến đúng giờ nhé! 😊"
            )

            return {
                "phase": "WAITING_APPROVAL",
                "active_request_id": str(booking.id),
                "active_request_code": booking.request_code,
                "pending_action": None,
                "selected_slots": [],
                "selected_slot_index": None,
                "response": enhanced_response,
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Kiểm tra trạng thái lịch", "Tìm thêm bất động sản"],
            }
        except (BookingConflictError, BookingNotFoundError, ValueError) as exc:
            return {
                "phase": "AWAITING_DATE",
                "selected_slots": [],
                "selected_slot_index": None,
                "response": f"Khung giờ này vừa có người đặt hoặc không còn khả dụng: {exc}. Bạn chọn ngày hoặc khung giờ khác giúp mình nhé.",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Chọn ngày khác"],
            }

    # ==========================================
    # 5. BOOK APPOINTMENT -> ASK DATE OR SHOW SLOTS
    # ==========================================
    # Find property
    prop_id = state.get("current_property_id")
    properties = state.get("selected_properties") or state.get("search_results") or []

    if not prop_id and properties:
        matched_idx, matched_prop = match_property_by_title(state.get("query", ""), properties)
        if matched_prop:
            prop_id = str(matched_prop["id"])
            state["current_property_id"] = prop_id
            state["selected_property_index"] = matched_idx
        elif len(properties) == 1:
            prop_id = properties[0]["id"]
            state["current_property_id"] = prop_id
        elif len(properties) > 1:
            return {
                "response": "Bạn muốn đặt lịch xem căn nào? Hãy chọn một căn trong danh sách (ví dụ: 'chọn căn số 1').",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [f"Chọn căn số {i}" for i in range(1, min(len(properties) + 1, 4))],
            }
        else:
            return {
                "response": "Hiện tại chưa có bất động sản nào được chọn trong danh sách. Bạn hãy tìm và chọn một căn ưng ý trước khi đặt lịch nhé!",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": ["Tìm căn hộ Quận 7", "Tìm nhà phố Hà Nội"],
            }
    elif not prop_id:
        return {
            "response": "Hiện tại chưa có bất động sản nào được chọn trong danh sách. Bạn hãy tìm và chọn một căn ưng ý trước khi đặt lịch nhé!",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": ["Tìm căn hộ Quận 7", "Tìm nhà phố Hà Nội"],
        }

    # Get Property Title
    async with get_session_context() as session:
        prop = await session.get(Property, UUID(prop_id))
        prop_title = clean_property_title(prop.title) if prop else "bất động sản"

    target_date_str = state.get("requested_date")
    if not target_date_str:
        return {
            "current_property_id": prop_id,
            "phase": "AWAITING_DATE",
            "pending_action": "CREATE_BOOKING",
            "response": f"Bạn muốn đi xem **{prop_title}** vào ngày nào? (Ví dụ: 'ngày mai', 'thứ Bảy tuần này'...).",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": ["Ngày mai", "Thứ Bảy tuần này", "Chủ Nhật tuần này"],
        }

    target_date = date.fromisoformat(target_date_str)
    if target_date < datetime.now(LOCAL_TZ).date():
        return {
            "current_property_id": prop_id,
            "phase": "AWAITING_DATE",
            "response": "Ngày xem nhà phải từ hôm nay trở đi. Bạn chọn lại một ngày trong tương lai nhé.",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": ["Hôm nay", "Ngày mai", "Cuối tuần này"],
        }

    async with get_session_context() as session:
        avail = await list_available_slots(session, UUID(prop_id), target_date)
        slots = avail.get("slots", [])

    req_hour = state.get("requested_hour")
    if req_hour is not None and slots:
        slots.sort(key=lambda s: abs(datetime.fromisoformat(s["starts_at"]).hour - req_hour))

    if not slots:
        return {
            "current_property_id": prop_id,
            "phase": "AWAITING_DATE",
            "pending_action": "CREATE_BOOKING",
            "response": f"Ngày {target_date.strftime('%d/%m/%Y')} hiện tại không còn khung giờ trống để xem căn **{prop_title}**. Bạn chọn ngày khác nhé.",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": ["Ngày mai", "Thứ Bảy", "Chủ Nhật"],
        }

    slot_actions = [f"Chọn khung giờ {i}" for i in range(1, len(slots) + 1)]
    return {
        "current_property_id": prop_id,
        "phase": "AWAITING_SLOT",
        "pending_action": "CREATE_BOOKING",
        "selected_slots": slots,
        "response": _format_slots_markdown(slots, prop_title, target_date),
        "current_agent": AgentType.RESPOND,
        "suggested_actions": slot_actions,
    }
