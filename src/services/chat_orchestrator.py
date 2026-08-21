"""Production chat orchestration built around trusted domain services.

This module intentionally lives outside ``src.agents``.  Language understanding
may be probabilistic, but property identifiers, availability, permissions and
booking side effects are always resolved and validated by this service layer.
"""

from __future__ import annotations

import logging
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import (
    Appointment,
    Property,
    PropertyKind,
    PropertyStatus,
    TourRequest,
    UserRole,
)
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
from src.services.chat_state_service import (
    LOCAL_TZ,
    extract_ordinal,
    is_affirmative,
    is_negative,
    normalize_text,
    parse_requested_date,
    parse_requested_hour,
)
from src.services.search_criteria_service import build_search_criteria, extract_search_criteria

logger = logging.getLogger(__name__)

PROPERTY_DETAIL_TERMS = (
    "chi tiet", "dien tich", "gia", "phong ngu", "phong tam", "dia chi",
    "phap ly", "mo ta", "tien ich", "huong", "view",
)
SEARCH_TERMS = (
    "tim", "can ho", "chung cu", "nha", "biet thu", "villa", "dat nen",
    "bat dong san", "ngan sach", "phong ngu", "quan ", "khu vuc", "du an",
)


def _number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


def serialize_property(prop: Property) -> dict[str, Any]:
    media = sorted(prop.media or [], key=lambda item: (not item.is_cover, item.sort_order))
    media_payload = [
        {
            "id": str(item.id),
            "media_type": item.media_type,
            "url": item.url,
            "caption": item.caption,
            "sort_order": item.sort_order,
            "is_cover": item.is_cover,
        }
        for item in media
    ]
    return {
        "id": str(prop.id),
        "code": prop.code,
        "property_kind": _enum_value(prop.property_kind),
        "title": prop.title,
        "description": str(prop.description)[:1500] if prop.description else None,
        "status": _enum_value(prop.status),
        "address_line": prop.address_line,
        "ward": prop.ward,
        "district": prop.district,
        "province": prop.province,
        "area_sqm": _number(prop.area_sqm),
        "bedrooms": prop.bedrooms,
        "bathrooms": prop.bathrooms,
        "list_price": _number(prop.list_price),
        "currency": prop.currency,
        # Crawled ``features`` also contains seller/source metadata. Do not send
        # that internal payload through chat; trusted user-facing columns above
        # are sufficient for matching and cards.
        "features": {},
        "media": media_payload,
        "image": media_payload[0]["url"] if media_payload else None,
    }


def _property_ref(item: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item.get(key)
        for key in (
            "id", "code", "title", "property_kind", "district", "province",
            "area_sqm", "bedrooms", "bathrooms", "list_price",
        )
    }


def _price_text(value: Any) -> str:
    amount = _number(value)
    if amount is None:
        return "Liên hệ"
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:g} tỷ"
    return f"{amount / 1_000_000:g} triệu"


def _property_summary(item: dict[str, Any], index: int | None = None) -> str:
    prefix = f"**{index}. " if index is not None else "**"
    location = ", ".join(filter(None, [item.get("district"), item.get("province")])) or "Chưa cập nhật"
    details = [
        _price_text(item.get("list_price")),
        f"{item.get('area_sqm'):g} m²" if item.get("area_sqm") else None,
        f"{item.get('bedrooms')} phòng ngủ" if item.get("bedrooms") is not None else None,
        location,
    ]
    return f"{prefix}{item.get('title', 'Bất động sản')}**\n" + " · ".join(part for part in details if part)


async def search_properties(
    db: AsyncSession,
    criteria: dict[str, Any],
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    filters = [Property.status == PropertyStatus.AVAILABLE]
    district = criteria.get("district")
    province = criteria.get("province")
    property_kind = criteria.get("property_kind")
    if district:
        filters.append(Property.district.ilike(f"%{str(district).strip()}%"))
    if province:
        filters.append(Property.province.ilike(f"%{str(province).strip()}%"))
    if property_kind:
        try:
            filters.append(Property.property_kind == PropertyKind(str(property_kind)))
        except ValueError:
            logger.warning("Ignoring invalid property kind: %s", property_kind)
    if criteria.get("min_price") is not None:
        filters.append(Property.list_price >= criteria["min_price"])
    if criteria.get("max_price") is not None:
        filters.append(Property.list_price <= criteria["max_price"])
    if criteria.get("min_bedrooms") is not None:
        filters.append(Property.bedrooms >= criteria["min_bedrooms"])
    if criteria.get("min_bathrooms") is not None:
        filters.append(Property.bathrooms >= criteria["min_bathrooms"])
    if criteria.get("min_area") is not None:
        filters.append(Property.area_sqm >= criteria["min_area"])

    statement = (
        select(Property)
        .options(selectinload(Property.media))
        .where(*filters)
        .order_by(Property.list_price.asc().nullslast(), Property.published_at.desc().nullslast())
        .limit(limit)
    )
    rows = (await db.execute(statement)).scalars().all()
    return [serialize_property(row) for row in rows]


async def _load_properties_by_refs(db: AsyncSession, refs: list[dict]) -> list[dict[str, Any]]:
    ids = []
    for item in refs:
        try:
            ids.append(UUID(str(item.get("id"))))
        except (TypeError, ValueError):
            continue
    if not ids:
        return []
    rows = (await db.execute(
        select(Property).options(selectinload(Property.media)).where(Property.id.in_(ids))
    )).scalars().all()
    by_id = {str(row.id): serialize_property(row) for row in rows}
    return [by_id[str(item["id"])] for item in refs if str(item.get("id")) in by_id]


def _is_selection_message(text: str) -> bool:
    if re.search(r"\b(phong ngu|pn|m2|ty|trieu)\b", text):
        return False
    return bool(re.search(r"\b(chon|can so|can thu|can dau|can cuoi|lua chon)\b", text))


def _is_booking_message(text: str) -> bool:
    return bool(re.search(r"\b(dat lich|xem nha|xem can|hen xem|tham quan)\b", text))


def _is_status_message(text: str) -> bool:
    return bool(re.search(r"\b(trang thai|lich cua toi|booking cua toi|kiem tra lich|ma booking)\b", text))


def _is_reschedule_message(text: str) -> bool:
    return bool(re.search(r"\b(doi lich|doi ngay|doi gio|chuyen lich|dat lai lich)\b", text))


def _extract_booking_code(message: str) -> str | None:
    match = re.search(r"\b(BK[A-Z0-9-]{5,}|TR-[A-Z0-9-]{5,})\b", message.upper())
    return match.group(1) if match else None


def _criteria_summary(criteria: dict[str, Any]) -> str:
    parts = []
    if criteria.get("district"):
        parts.append(str(criteria["district"]))
    elif criteria.get("province"):
        parts.append(str(criteria["province"]))
    kind_names = {
        "APARTMENT": "căn hộ", "HOUSE": "nhà riêng", "VILLA": "biệt thự",
        "TOWNHOUSE": "nhà phố", "LAND": "đất", "COMMERCIAL": "bất động sản thương mại",
    }
    if criteria.get("property_kind"):
        parts.append(kind_names.get(str(criteria["property_kind"]), str(criteria["property_kind"])))
    if criteria.get("max_price") is not None:
        parts.append(f"tối đa {_price_text(criteria['max_price'])}")
    if criteria.get("min_price") is not None:
        parts.append(f"từ {_price_text(criteria['min_price'])}")
    if criteria.get("min_bedrooms") is not None:
        parts.append(f"{criteria['min_bedrooms']}+ phòng ngủ")
    if criteria.get("min_area") is not None:
        parts.append(f"từ {criteria['min_area']:g} m²")
    return ", ".join(parts)


def _format_search_results(items: list[dict[str, Any]], criteria: dict[str, Any]) -> str:
    heading = "Mình tìm thấy các căn phù hợp"
    summary = _criteria_summary(criteria)
    if summary:
        heading += f" với tiêu chí **{summary}**"
    body = "\n\n".join(_property_summary(item, index) for index, item in enumerate(items, 1))
    return f"{heading}:\n\n{body}\n\nBạn chọn căn số mấy, hoặc muốn điều chỉnh tiêu chí nào?"


def _format_property_details(item: dict[str, Any]) -> str:
    lines = [_property_summary(item)]
    if item.get("address_line"):
        lines.append(f"- Địa chỉ: {item['address_line']}")
    lines.append(f"- Loại: {item.get('property_kind') or 'Chưa cập nhật'}")
    lines.append(f"- Phòng tắm: {item.get('bathrooms') if item.get('bathrooms') is not None else 'Chưa cập nhật'}")
    features = item.get("features")
    if features:
        if isinstance(features, dict):
            feature_text = ", ".join(str(key) for key, value in features.items() if value)
        elif isinstance(features, list):
            feature_text = ", ".join(map(str, features))
        else:
            feature_text = str(features)
        if feature_text:
            lines.append(f"- Tiện ích/đặc điểm: {feature_text}")
    if item.get("description"):
        lines.append(f"- Mô tả: {str(item['description'])[:500]}")
    lines.append("\nBạn muốn đặt lịch xem căn này vào ngày nào?")
    return "\n".join(lines)


def _format_comparison(items: list[dict[str, Any]]) -> str:
    lines = ["Đây là so sánh dựa trên dữ liệu đang có trong hệ thống:"]
    for index, item in enumerate(items, 1):
        lines.append(
            f"\n**{index}. {item['title']}**\n"
            f"- Giá: {_price_text(item.get('list_price'))}\n"
            f"- Diện tích: {item.get('area_sqm') or 'Chưa cập nhật'} m²\n"
            f"- Phòng ngủ: {item.get('bedrooms') if item.get('bedrooms') is not None else 'Chưa cập nhật'}\n"
            f"- Khu vực: {item.get('district') or item.get('province') or 'Chưa cập nhật'}"
        )
    lines.append("\nBạn muốn xem chi tiết hoặc đặt lịch căn số mấy?")
    return "\n".join(lines)


def _format_slots(slots: list[dict[str, Any]], property_title: str, target_date: date) -> str:
    weekday_names = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật")
    lines = [
        f"Các khung giờ còn trống để xem **{property_title}** vào "
        f"**{weekday_names[target_date.weekday()]}, {target_date.strftime('%d/%m/%Y')}**:"
    ]
    for index, slot in enumerate(slots, 1):
        start = datetime.fromisoformat(slot["starts_at"])
        end = datetime.fromisoformat(slot["ends_at"])
        lines.append(
            f"\n**{index}. {start.strftime('%H:%M')}–{end.strftime('%H:%M')}** · Sale {slot['sale_name']}"
        )
    lines.append("\nBạn chọn khung giờ số mấy?")
    return "\n".join(lines)


async def _find_request(
    db: AsyncSession,
    customer_id: UUID,
    code: str | None,
    state: dict[str, Any],
) -> UUID | None:
    if code:
        statement = (
            select(TourRequest.id)
            .outerjoin(Appointment, Appointment.tour_request_id == TourRequest.id)
            .where(
                TourRequest.customer_user_id == customer_id,
                or_(TourRequest.request_code == code, Appointment.booking_code == code),
            )
        )
        return await db.scalar(statement)
    try:
        return UUID(str(state.get("active_request_id")))
    except (TypeError, ValueError):
        return None


async def _show_bookings(db: AsyncSession, customer_id: UUID) -> str:
    bookings = await get_my_tour_requests(db, customer_id)
    if not bookings:
        return "Bạn chưa có yêu cầu xem nhà nào. Mình có thể giúp bạn tìm một căn phù hợp trước."
    lines = ["Các lịch xem gần đây của bạn:"]
    for booking in bookings[:5]:
        prop = booking.property.title if booking.property else "Bất động sản"
        when = booking.preferred_start.astimezone(LOCAL_TZ).strftime("%d/%m/%Y %H:%M")
        code = booking.appointment.booking_code if booking.appointment else booking.request_code
        lines.append(f"\n- **{code}** · {prop} · {when} · {booking.status}")
    lines.append("\nBạn có thể gửi mã để mình kiểm tra, hủy hoặc dời lịch.")
    return "".join(lines)


async def _prepare_slots(
    db: AsyncSession,
    state: dict[str, Any],
    property_item: dict[str, Any],
    target_date: date,
    requested_hour: int | None,
    *,
    action: str,
) -> dict[str, Any]:
    if target_date < datetime.now(LOCAL_TZ).date():
        return {"response": "Ngày xem phải từ hôm nay trở đi. Bạn muốn chọn ngày nào khác?"}
    availability = await list_available_slots(db, UUID(property_item["id"]), target_date)
    slots = availability.get("slots", [])
    if requested_hour is not None:
        slots.sort(key=lambda item: abs(datetime.fromisoformat(item["starts_at"]).hour - requested_hour))
    if not slots:
        state.update({
            "phase": "AWAITING_DATE",
            "requested_date": target_date.isoformat(),
            "requested_hour": requested_hour,
            "slots": [],
            "pending_action": action,
        })
        return {
            "response": (
                f"Ngày {target_date.strftime('%d/%m/%Y')} chưa còn khung giờ phù hợp cho căn này. "
                "Bạn chọn ngày khác nhé."
            )
        }
    state.update({
        "phase": "AWAITING_SLOT",
        "requested_date": target_date.isoformat(),
        "requested_hour": requested_hour,
        "slots": slots,
        "selected_slot_index": None,
        "pending_action": action,
    })
    return {"response": _format_slots(slots, property_item["title"], target_date)}


async def _complete_slot_action(
    db: AsyncSession,
    state: dict[str, Any],
    slot_index: int,
    *,
    customer_id: UUID | None,
    user_role: UserRole | None,
) -> dict[str, Any]:
    slots = state.get("slots") or []
    if slot_index < 0 or slot_index >= len(slots):
        return {"response": f"Mình chỉ có {len(slots)} khung giờ trong danh sách. Bạn chọn lại giúp mình nhé."}
    state["selected_slot_index"] = slot_index
    if customer_id is None:
        state["phase"] = "AWAITING_AUTH"
        return {
            "response": (
                "Mình đã giữ lựa chọn của bạn trong cuộc trò chuyện. Bạn cần **đăng nhập tài khoản khách hàng** "
                "để gửi yêu cầu cho Sale; sau khi đăng nhập, hãy nhắn “tiếp tục”."
            ),
            "auth_required": True,
        }
    if user_role != UserRole.CUSTOMER:
        return {"response": "Chỉ tài khoản Khách hàng mới có thể đặt lịch xem nhà."}

    property_id = state.get("selected_property_id")
    if not property_id:
        state["phase"] = "IDLE"
        return {"response": "Mình không còn xác định được căn đã chọn. Bạn vui lòng tìm và chọn lại căn."}
    slot = slots[slot_index]
    start = datetime.fromisoformat(slot["starts_at"])
    end = datetime.fromisoformat(slot["ends_at"])
    action = str(state.get("pending_action") or "CREATE_BOOKING")
    try:
        if action.startswith("RESCHEDULE:"):
            request_id = UUID(action.split(":", 1)[1])
            booking = await reschedule_customer_booking(
                db,
                request_id,
                customer_id,
                UUID(slot["sale_user_id"]),
                start,
                end,
            )
            verb = "dời lịch"
        else:
            row = await create_tour_request(
                db,
                customer_id,
                TourRequestCreate(
                    property_id=UUID(property_id),
                    sale_user_id=UUID(slot["sale_user_id"]),
                    preferred_start=start,
                    preferred_end=end,
                    pax_count=1,
                ),
            )
            booking = await get_customer_booking(db, row.id, customer_id)
            verb = "gửi yêu cầu"
    except (BookingConflictError, BookingNotFoundError, ValueError) as exc:
        state.update({"phase": "AWAITING_DATE", "slots": [], "selected_slot_index": None})
        return {"response": f"Khung giờ này vừa không còn khả dụng: {exc}. Bạn chọn ngày hoặc giờ khác nhé."}

    state.update({
        "phase": "AWAITING_APPROVAL",
        "active_request_id": str(booking.id),
        "active_request_code": booking.request_code,
        "pending_action": None,
    })
    local_start = booking.preferred_start.astimezone(LOCAL_TZ)
    return {
        "response": (
            f"✅ Đã {verb} thành công.\n\n"
            f"- Mã yêu cầu: **{booking.request_code}**\n"
            f"- Thời gian: **{local_start.strftime('%H:%M, %d/%m/%Y')}**\n"
            f"- Trạng thái: **WAITING_APPROVAL – chờ Sale xác nhận**\n\n"
            "Bạn có thể dùng mã trên để kiểm tra trạng thái. Hệ thống sẽ thông báo khi Sale phản hồi."
        )
    }


async def orchestrate_chat(
    db: AsyncSession,
    message: str,
    state: dict[str, Any],
    *,
    customer_id: UUID | None,
    user_role: UserRole | None,
    initial_property_id: UUID | None = None,
    llm_understanding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Process one user turn and mutate the supplied JSON state in place."""
    text = normalize_text(message)
    understanding = llm_understanding or {}
    llm_intent = str(understanding.get("intent") or "")
    llm_direct_response = str(understanding.get("direct_response") or "").strip()
    llm_affirmative = llm_intent == "AFFIRM"
    llm_negative = llm_intent == "DENY"
    refs = state.get("property_refs") or []
    if initial_property_id and not any(str(item.get("id")) == str(initial_property_id) for item in refs):
        loaded = await _load_properties_by_refs(db, [{"id": str(initial_property_id)}])
        if loaded:
            refs = [_property_ref(loaded[0])]
            state.update({
                "property_refs": refs,
                "selected_property_id": str(initial_property_id),
                "selected_property_index": 0,
                "phase": "PROPERTY_SELECTED",
            })
    current_properties = await _load_properties_by_refs(db, refs)

    # Resume a pre-login booking without asking the customer to repeat a slot.
    if state.get("phase") == "AWAITING_AUTH" and customer_id and (is_affirmative(message) or llm_affirmative):
        index = state.get("selected_slot_index")
        if isinstance(index, int):
            result = await _complete_slot_action(
                db, state, index, customer_id=customer_id, user_role=user_role
            )
            result["properties"] = current_properties
            return result

    if re.fullmatch(r"(xin )?chao|hello|hi|alo", text) or llm_intent == "SMALLTALK":
        if llm_direct_response:
            return {
                "response": llm_direct_response,
                "properties": current_properties,
                "response_kind": "LLM_DIRECT",
            }
        return {
            "response": (
                "Xin chào! Mình là Nera. Mình có thể tìm nhà theo khu vực, ngân sách và nhu cầu; "
                "sau đó giúp bạn gửi lịch xem cho Sale. Bạn đang tìm nhà ở đâu?"
            ),
            "properties": current_properties,
        }
    if re.fullmatch(r"cam on|thanks|thank you", text):
        return {"response": "Rất vui được hỗ trợ bạn. Bạn muốn xem thêm căn nào không?", "properties": current_properties}
    if re.fullmatch(r"tam biet|bye|goodbye", text):
        return {"response": "Tạm biệt bạn! Khi cần tìm hoặc đặt lịch xem nhà, cứ quay lại nhắn mình nhé."}

    code = understanding.get("booking_code") or _extract_booking_code(message)
    if text.startswith("huy") or "huy lich" in text or llm_intent == "CANCEL_BOOKING":
        if customer_id is None:
            return {"response": "Bạn cần đăng nhập để hủy lịch của mình.", "auth_required": True}
        request_id = await _find_request(db, customer_id, code, state)
        if not request_id:
            return {"response": "Bạn muốn hủy lịch nào? Hãy gửi mã TR-… hoặc BK… của lịch đó."}
        state.update({"phase": "AWAITING_CANCEL_CONFIRMATION", "active_request_id": str(request_id)})
        return {"response": "Bạn xác nhận muốn hủy lịch này chứ? Hãy trả lời **xác nhận** hoặc **không**."}

    if state.get("phase") == "AWAITING_CANCEL_CONFIRMATION":
        if is_negative(message) or llm_negative:
            state.update({"phase": "IDLE", "pending_action": None})
            return {"response": "Đã giữ nguyên lịch của bạn."}
        if is_affirmative(message) or llm_affirmative:
            if customer_id is None:
                return {"response": "Phiên đăng nhập đã hết. Bạn đăng nhập lại để hủy lịch nhé.", "auth_required": True}
            request_id = await _find_request(db, customer_id, None, state)
            if not request_id:
                state["phase"] = "IDLE"
                return {"response": "Không tìm thấy lịch cần hủy."}
            booking = await cancel_customer_booking(db, request_id, customer_id, "Khách hàng yêu cầu qua chatbot")
            state.update({"phase": "IDLE", "pending_action": None})
            return {"response": f"✅ Đã hủy lịch **{booking.request_code}**. Sale sẽ nhận được thông báo."}
        return {"response": "Vui lòng trả lời **xác nhận** nếu bạn muốn hủy, hoặc **không** để giữ lịch."}

    if (
        _is_status_message(text)
        or llm_intent in {"LIST_BOOKINGS", "BOOKING_STATUS"}
        or (code and not _is_booking_message(text))
    ):
        if customer_id is None:
            return {"response": "Bạn cần đăng nhập để xem trạng thái lịch của mình.", "auth_required": True}
        request_id = await _find_request(db, customer_id, code, state)
        if not request_id:
            return {"response": await _show_bookings(db, customer_id)}
        booking = await get_customer_booking(db, request_id, customer_id)
        state.update({"active_request_id": str(booking.id), "active_request_code": booking.request_code})
        appointment_code = booking.appointment.booking_code if booking.appointment else None
        response = (
            f"Trạng thái yêu cầu **{booking.request_code}**: **{booking.status}**.\n"
            f"- Căn: {booking.property.title if booking.property else 'Chưa cập nhật'}\n"
            f"- Thời gian: {booking.preferred_start.astimezone(LOCAL_TZ).strftime('%H:%M, %d/%m/%Y')}"
        )
        if appointment_code:
            response += f"\n- Mã booking đã xác nhận: **{appointment_code}**"
        return {"response": response}

    if (
        _is_reschedule_message(text)
        or llm_intent == "RESCHEDULE_BOOKING"
        or state.get("pending_action") == "RESCHEDULE_PENDING_DATE"
    ):
        if customer_id is None:
            return {"response": "Bạn cần đăng nhập để dời lịch của mình.", "auth_required": True}
        request_id = await _find_request(db, customer_id, code, state)
        if not request_id:
            return {"response": "Bạn muốn dời lịch nào? Hãy gửi kèm mã TR-… hoặc BK…."}
        booking = await get_customer_booking(db, request_id, customer_id)
        target_date = parse_requested_date(message)
        if target_date is None and understanding.get("requested_date"):
            try:
                target_date = date.fromisoformat(str(understanding["requested_date"]))
            except ValueError:
                target_date = None
        state.update({
            "active_request_id": str(request_id),
            "selected_property_id": str(booking.property.id),
            "pending_action": "RESCHEDULE_PENDING_DATE",
            "phase": "AWAITING_DATE",
        })
        if not target_date:
            return {"response": "Bạn muốn chuyển lịch sang ngày nào? Ví dụ: “14 giờ thứ Bảy tuần sau”."}
        property_item = (await _load_properties_by_refs(db, [{"id": str(booking.property.id)}]))[0]
        state["property_refs"] = [_property_ref(property_item)]
        return await _prepare_slots(
            db,
            state,
            property_item,
            target_date,
            understanding.get("requested_hour") or parse_requested_hour(message),
            action=f"RESCHEDULE:{request_id}",
        )

    # Slot selection is intentionally checked before property ordinal selection.
    if state.get("phase") == "AWAITING_SLOT":
        slot_index = extract_ordinal(message, maximum=len(state.get("slots") or []))
        if slot_index is None and isinstance(understanding.get("property_ordinal"), int):
            candidate = int(understanding["property_ordinal"]) - 1
            if 0 <= candidate < len(state.get("slots") or []):
                slot_index = candidate
        if slot_index is not None:
            result = await _complete_slot_action(
                db, state, slot_index, customer_id=customer_id, user_role=user_role
            )
            result["properties"] = current_properties
            return result

    property_index = None
    if refs and (_is_selection_message(text) or llm_intent == "SELECT_PROPERTY"):
        property_index = extract_ordinal(message, maximum=len(refs))
        if property_index is None and isinstance(understanding.get("property_ordinal"), int):
            candidate = int(understanding["property_ordinal"]) - 1
            if 0 <= candidate < len(refs):
                property_index = candidate
        if property_index is None:
            return {"response": f"Danh sách hiện có {len(refs)} căn. Bạn chọn số từ 1 đến {len(refs)} nhé.", "properties": current_properties}
        selected = refs[property_index]
        state.update({
            "selected_property_id": selected["id"],
            "selected_property_index": property_index,
            "phase": "PROPERTY_SELECTED",
        })

    selected_property = None
    if state.get("selected_property_id"):
        selected_property = next(
            (item for item in current_properties if item["id"] == state["selected_property_id"]),
            None,
        )
    if property_index is not None and selected_property is None and property_index < len(current_properties):
        selected_property = current_properties[property_index]

    if ("so sanh" in text or llm_intent == "COMPARE") and len(current_properties) >= 2:
        return {
            "response": _format_comparison(current_properties[:3]),
            "properties": current_properties[:3],
            "response_kind": "PROPERTY_ADVICE",
        }

    booking_requested = _is_booking_message(text) or llm_intent == "CREATE_BOOKING"
    if booking_requested or state.get("phase") == "AWAITING_DATE":
        if selected_property is None:
            if len(current_properties) == 1:
                selected_property = current_properties[0]
                state.update({"selected_property_id": selected_property["id"], "selected_property_index": 0})
            else:
                return {
                    "response": "Bạn muốn đặt lịch xem căn nào? Hãy chọn một căn trong danh sách, ví dụ “chọn căn số 1”.",
                    "properties": current_properties,
                }
        target_date = parse_requested_date(message)
        if target_date is None and understanding.get("requested_date"):
            try:
                target_date = date.fromisoformat(str(understanding["requested_date"]))
            except ValueError:
                target_date = None
        if target_date is None:
            state.update({"phase": "AWAITING_DATE", "pending_action": "CREATE_BOOKING"})
            return {
                "response": f"Bạn muốn xem **{selected_property['title']}** vào ngày nào?",
                "properties": [selected_property],
            }
        result = await _prepare_slots(
            db,
            state,
            selected_property,
            target_date,
            understanding.get("requested_hour") or parse_requested_hour(message),
            action="CREATE_BOOKING",
        )
        result["properties"] = [selected_property]
        return result

    if property_index is not None and selected_property:
        return {
            "response": (
                f"Bạn đã chọn **{selected_property['title']}**. "
                "Bạn muốn xem chi tiết hay đặt lịch vào ngày nào?"
            ),
            "properties": [selected_property],
        }

    if selected_property and (
        any(term in text for term in PROPERTY_DETAIL_TERMS)
        or llm_intent == "PROPERTY_DETAILS"
    ):
        return {
            "response": _format_property_details(selected_property),
            "properties": [selected_property],
            "response_kind": "PROPERTY_ADVICE",
        }

    explicit, _ = extract_search_criteria(message)
    hard_criteria = understanding.get("hard_criteria") or {}
    llm_explicit = {
        key: value
        for key, value in hard_criteria.items()
        if value is not None
    } if isinstance(hard_criteria, dict) else {}
    should_search = (
        bool(explicit)
        or bool(llm_explicit)
        or llm_intent in {"SEARCH", "REFINE_SEARCH"}
        or any(term in text for term in SEARCH_TERMS)
    )
    if should_search:
        previous = {} if understanding.get("is_new_search") else (state.get("criteria") or {})
        criteria = build_search_criteria(message, previous)
        if llm_explicit.get("district") or llm_explicit.get("province"):
            criteria.pop("district", None)
            criteria.pop("province", None)
        if llm_explicit.get("min_price") is not None or llm_explicit.get("max_price") is not None:
            criteria.pop("min_price", None)
            criteria.pop("max_price", None)
        criteria.update(llm_explicit)
        if not criteria:
            return {
                "response": (
                    "Để tìm chính xác hơn, bạn cho mình ít nhất một tiêu chí nhé: khu vực, ngân sách, "
                    "loại nhà hoặc số phòng ngủ."
                )
            }
        properties = await search_properties(db, criteria)
        state.update({
            "criteria": criteria,
            "soft_preferences": understanding.get("soft_preferences") or [],
            "household_context": understanding.get("household_context") or [],
            "commute_landmark": understanding.get("commute_landmark"),
            "max_commute_minutes": understanding.get("max_commute_minutes"),
            "property_refs": [_property_ref(item) for item in properties],
            "selected_property_id": None,
            "selected_property_index": None,
            "slots": [],
            "phase": "SEARCH_RESULTS" if properties else "SEARCH_NO_RESULTS",
            "pending_action": None,
        })
        if not properties:
            summary = _criteria_summary(criteria)
            return {
                "response": (
                    f"Mình chưa tìm thấy căn nào khớp **{summary or 'các tiêu chí hiện tại'}**. "
                    "Bạn có thể tăng ngân sách, đổi khu vực hoặc giảm số phòng ngủ; mình sẽ giữ các tiêu chí còn lại."
                ),
                "properties": [],
                "insights": criteria,
                "response_kind": "SEARCH_NO_RESULTS",
            }
        return {
            "response": _format_search_results(properties, criteria),
            "properties": properties,
            "insights": criteria,
            "response_kind": "SEARCH_RESULTS",
        }

    if llm_direct_response and llm_intent in {"OUT_OF_SCOPE", "UNKNOWN"}:
        return {
            "response": llm_direct_response,
            "properties": current_properties,
            "response_kind": "LLM_DIRECT",
        }
    return {
        "response": (
            "Mình hỗ trợ tìm bất động sản, xem thông tin có trong hệ thống và đặt/hủy/dời lịch xem nhà. "
            "Bạn có thể nói tự nhiên, ví dụ: “Tìm căn hộ 2 phòng ngủ ở Quận 7 dưới 5 tỷ”."
        ),
        "properties": current_properties,
        "response_kind": "OUT_OF_SCOPE",
    }
