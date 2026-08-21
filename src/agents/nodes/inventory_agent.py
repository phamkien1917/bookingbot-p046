"""Inventory Agent - Property Search, Details, and Comparison.

Queries real estate database with exact SQL constraints and formats grounded responses.
"""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.agents.state import AgentState, AgentType, Intent
from src.database.connection import get_session_context
from src.database.models import Property, PropertyKind, PropertyStatus

logger = logging.getLogger(__name__)


def _num(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _price_text(value: Any) -> str:
    amount = _num(value)
    if amount is None:
        return "Liên hệ"
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:g} tỷ"
    return f"{amount / 1_000_000:g} triệu"


def serialize_property_item(prop: Property) -> dict[str, Any]:
    """Serialize Property model to JSON-safe dictionary for cards and prompt context."""
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
        "property_kind": prop.property_kind.value if prop.property_kind else None,
        "title": prop.title,
        "description": str(prop.description)[:1200] if prop.description else None,
        "status": prop.status.value if prop.status else None,
        "address_line": prop.address_line,
        "ward": prop.ward,
        "district": prop.district,
        "province": prop.province,
        "area_sqm": _num(prop.area_sqm),
        "bedrooms": prop.bedrooms,
        "bathrooms": prop.bathrooms,
        "list_price": _num(prop.list_price),
        "currency": prop.currency,
        "media": media_payload,
        "image": media_payload[0]["url"] if media_payload else None,
    }


async def query_properties_from_db(criteria: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    """Execute dynamic criteria search against PostgreSQL with relationship eager-loading."""
    async with get_session_context() as session:
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
                pass

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

        stmt = (
            select(Property)
            .options(selectinload(Property.media))
            .where(*filters)
            .order_by(Property.list_price.asc().nullslast(), Property.published_at.desc().nullslast())
            .limit(limit)
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [serialize_property_item(r) for r in rows]


async def load_properties_by_ids(ids: list[str]) -> list[dict[str, Any]]:
    """Load full property items for a list of UUIDs."""
    parsed_ids = []
    for raw in ids:
        try:
            parsed_ids.append(UUID(str(raw)))
        except (ValueError, TypeError):
            continue
    if not parsed_ids:
        return []

    async with get_session_context() as session:
        stmt = (
            select(Property)
            .options(selectinload(Property.media))
            .where(Property.id.in_(parsed_ids))
        )
        rows = (await session.execute(stmt)).scalars().all()
        by_id = {str(r.id): serialize_property_item(r) for r in rows}
        return [by_id[str(raw)] for raw in ids if str(raw) in by_id]


def format_criteria_summary(criteria: dict[str, Any]) -> str:
    parts = []
    if criteria.get("district"):
        parts.append(str(criteria["district"]))
    elif criteria.get("province"):
        parts.append(str(criteria["province"]))

    kind_names = {
        "APARTMENT": "căn hộ",
        "HOUSE": "nhà riêng",
        "VILLA": "biệt thự",
        "TOWNHOUSE": "nhà phố",
        "LAND": "đất nền",
        "COMMERCIAL": "mặt bằng kinh doanh",
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


def format_search_results_markdown(items: list[dict[str, Any]], criteria: dict[str, Any], soft_prefs: list[str]) -> str:
    heading = "Mình đã tìm thấy các bất động sản phù hợp"
    summary = format_criteria_summary(criteria)
    if summary:
        heading += f" với tiêu chí **{summary}**"
    heading += ":"

    blocks = []
    for index, item in enumerate(items, 1):
        location = ", ".join(filter(None, [item.get("district"), item.get("province")])) or "Chưa cập nhật"
        facts = [
            _price_text(item.get("list_price")),
            f"{item.get('area_sqm'):g} m²" if item.get("area_sqm") else None,
            f"{item.get('bedrooms')} phòng ngủ" if item.get("bedrooms") is not None else None,
            location,
        ]
        fact_line = " · ".join(part for part in facts if part)
        blocks.append(f"**{index}. {item.get('title', 'Bất động sản')}**\n{fact_line}")

    body = "\n\n".join(blocks)

    note = ""
    if soft_prefs:
        note = f"\n\n*(Đã cân nhắc thêm mong muốn: {', '.join(soft_prefs)})*"

    return f"{heading}\n\n{body}{note}\n\nBạn muốn chọn căn số mấy để xem chi tiết hoặc đặt lịch xem nhà?"


def format_property_details_markdown(item: dict[str, Any]) -> str:
    location = ", ".join(filter(None, [item.get("address_line"), item.get("ward"), item.get("district"), item.get("province")]))
    lines = [
        f"**{item.get('title', 'Thông tin Bất động sản')}**\n",
        f"- 💰 **Giá niêm yết:** {_price_text(item.get('list_price'))}",
        f"- 📐 **Diện tích:** {item.get('area_sqm') or 'Chưa cập nhật'} m²",
        f"- 🛏️ **Phòng ngủ:** {item.get('bedrooms') if item.get('bedrooms') is not None else 'Chưa cập nhật'}",
        f"- 🚿 **Phòng tắm/WC:** {item.get('bathrooms') if item.get('bathrooms') is not None else 'Chưa cập nhật'}",
        f"- 📍 **Địa chỉ:** {location or 'Chưa cập nhật'}",
        f"- 🏷️ **Loại BĐS:** {item.get('property_kind') or 'Chưa cập nhật'}",
        f"- 📋 **Mã căn:** `{item.get('code') or item.get('id')}`",
    ]
    if item.get("description"):
        lines.append(f"- 📝 **Mô tả:** {str(item['description'])[:450]}")

    lines.append("\nBạn có muốn mình kiểm tra lịch trống và hỗ trợ **đặt lịch xem căn này** không?")
    return "\n".join(lines)


def format_comparison_markdown(items: list[dict[str, Any]]) -> str:
    lines = ["📊 **Bảng so sánh nhanh các bất động sản bạn đang quan tâm:**\n"]
    for index, item in enumerate(items, 1):
        location = ", ".join(filter(None, [item.get("district"), item.get("province")]))
        lines.append(
            f"**{index}. {item['title']}**\n"
            f"- 💰 Giá: **{_price_text(item.get('list_price'))}**\n"
            f"- 📐 Diện tích: {item.get('area_sqm') or '—'} m² | {item.get('bedrooms') or '—'} PN | {item.get('bathrooms') or '—'} WC\n"
            f"- 📍 Vị trí: {location}\n"
        )
    lines.append("Bạn muốn xem chi tiết hoặc đặt lịch đi xem căn số mấy?")
    return "\n".join(lines)


async def inventory_agent(state: AgentState) -> dict[str, Any]:
    """Inventory Agent node: handles searching, selecting, detailing, and comparing properties."""
    intent = state.get("intent")
    criteria = state.get("search_criteria", {})
    existing_properties = state.get("selected_properties", [])
    soft_prefs = state.get("soft_preferences", [])
    current_prop_id = state.get("current_property_id")
    selected_idx = state.get("selected_property_index")

    # Step 1: Handle COMPARE_PROPERTIES
    if intent == Intent.COMPARE_PROPERTIES:
        props = existing_properties
        if len(props) < 2:
            # Query top available properties in the same area to compare
            alt_criteria = {}
            if criteria.get("district"):
                alt_criteria["district"] = criteria["district"]
            if criteria.get("province"):
                alt_criteria["province"] = criteria["province"]
            if criteria.get("property_kind"):
                alt_criteria["property_kind"] = criteria["property_kind"]
            props = await query_properties_from_db(alt_criteria, limit=3)

        if props:
            return {
                "selected_properties": props,
                "comparison_properties": props[:3],
                "response": format_comparison_markdown(props[:3]),
                "response_kind": "PROPERTY_ADVICE",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    f"Chọn căn số 1",
                    f"Chọn căn số 2" if len(props) >= 2 else "Đặt lịch xem",
                    "Đặt lịch xem nhà",
                ],
            }

    # Step 2: Handle PROPERTY_DETAILS (Evaluated before selection to answer questions on selected property!)
    if intent == Intent.PROPERTY_DETAILS:
        chosen = None
        if current_prop_id and existing_properties:
            chosen = next((p for p in existing_properties if p.get("id") == current_prop_id), None)
        if not chosen and existing_properties:
            if selected_idx is not None and 0 <= selected_idx < len(existing_properties):
                chosen = existing_properties[selected_idx]
            else:
                chosen = existing_properties[0]
        if not chosen and current_prop_id:
            loaded = await load_properties_by_ids([current_prop_id])
            if loaded:
                chosen = loaded[0]

        if chosen:
            return {
                "current_property_id": chosen["id"],
                "selected_properties": [chosen],
                "response": format_property_details_markdown(chosen),
                "response_kind": "PROPERTY_ADVICE",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    "Đặt lịch xem căn này",
                    "Hỏi thêm thông tin",
                    "Tìm căn khác",
                ],
            }

    # Step 3: Handle SELECT_PROPERTY
    if intent == Intent.SELECT_PROPERTY:
        if existing_properties:
            if selected_idx is not None and 0 <= selected_idx < len(existing_properties):
                chosen = existing_properties[selected_idx]
            elif current_prop_id:
                chosen = next((p for p in existing_properties if p.get("id") == current_prop_id), existing_properties[0])
            else:
                chosen = existing_properties[0]

            return {
                "current_property_id": chosen["id"],
                "selected_property_index": selected_idx if selected_idx is not None else 0,
                "selected_properties": [chosen],
                "response": f"Bạn đã chọn **{chosen['title']}** ({_price_text(chosen.get('list_price'))}, {chosen.get('area_sqm')} m² tại {chosen.get('district')}).\n\nBạn muốn xem chi tiết hay đặt lịch xem căn này vào ngày nào?",
                "response_kind": "PROPERTY_SELECTED",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    "Xem chi tiết căn này",
                    "Đặt lịch xem ngày mai",
                    "Đặt lịch thứ Bảy tuần này",
                    "Tìm căn khác",
                ],
            }

    # Step 4: Default -> SEARCH_PROPERTY
    if not criteria or not any(criteria.values()):
        return {
            "response": "Để mình tìm được căn hộ/nhà đất ưng ý nhất cho bạn, bạn chia sẻ thêm một vài thông tin nhé:\n- **Khu vực mong muốn** (ví dụ: Quận 7, Cầu Giấy, Bình Thạnh...)\n- **Khoảng ngân sách** (ví dụ: dưới 5 tỷ, 15-20 triệu/tháng...)\n- **Loại hình & số phòng ngủ** (ví dụ: căn hộ 2PN, nhà phố...)",
            "response_kind": "ASK_CRITERIA",
            "phase": "IDLE",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                "Căn hộ Quận 7 dưới 5 tỷ",
                "Nhà riêng Cầu Giấy 3 phòng ngủ",
                "Chung cư 2PN gần trung tâm",
            ],
        }

    properties = await query_properties_from_db(criteria, limit=5)

    if not properties:
        summary = format_criteria_summary(criteria)
        return {
            "selected_properties": [],
            "response": f"Rất tiếc mình chưa tìm thấy bất động sản nào khớp hoàn toàn với tiêu chí **{summary or 'hiện tại'}**.\n\n💡 **Gợi ý điều chỉnh:**\n- Thử nới rộng ngân sách hoặc mở rộng sang các quận lân cận\n- Giảm bớt yêu cầu số phòng ngủ hoặc diện tích tối thiểu\n\nMình vẫn đang giữ các tiêu chí khác của bạn. Bạn muốn điều chỉnh phần nào?",
            "response_kind": "SEARCH_NO_RESULTS",
            "phase": "SEARCH_NO_RESULTS",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                "Tăng ngân sách lên",
                "Mở rộng khu vực lân cận",
                "Xem tất cả căn đang có",
            ],
        }

    suggested_actions = [f"Chọn căn số {i}" for i in range(1, min(len(properties) + 1, 4))]
    if len(properties) >= 2:
        suggested_actions.append("So sánh các căn này")

    return {
        "selected_properties": properties,
        "current_property_id": None,
        "selected_property_index": None,
        "response": format_search_results_markdown(properties, criteria, soft_prefs),
        "response_kind": "SEARCH_RESULTS",
        "phase": "SEARCH_RESULTS",
        "current_agent": AgentType.RESPOND,
        "suggested_actions": suggested_actions,
    }
