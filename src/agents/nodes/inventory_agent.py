"""Inventory Agent - Property Search, Details, and Comparison.

Queries real estate database with exact SQL constraints and formats grounded responses.
"""

import json
import logging
import re
from decimal import Decimal
from typing import Any
from uuid import UUID

from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.agents.state import AgentState, AgentType, Intent
from src.database.connection import get_session_context
from src.database.models import Property, PropertyKind, PropertyStatus
from src.services.llm import get_llm

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
    summary = format_criteria_summary(criteria)
    intro = f"Nera đã tìm thấy **{len(items)} bất động sản** phù hợp nhất"
    if summary:
        intro += f" với tiêu chí **{summary}**"
    intro += " cho bạn:\n"

    blocks = []
    for index, item in enumerate(items, 1):
        location = ", ".join(filter(None, [item.get("district"), item.get("province")])) or "Chưa cập nhật"
        price = _price_text(item.get("list_price"))
        area = f"{item.get('area_sqm'):g} m²" if item.get("area_sqm") else ""
        beds = f"{item.get('bedrooms')} PN" if item.get("bedrooms") is not None else ""
        specs = " · ".join(filter(None, [price, area, beds, location]))
        blocks.append(f"**{index}. {item.get('title', 'Bất động sản')}**\n{specs}")

    body = "\n\n".join(blocks)
    note = f"\n\n*(Đã cân nhắc thêm: {', '.join(soft_prefs)})*" if soft_prefs else ""

    return f"{intro}\n{body}{note}\n\nBạn muốn xem chi tiết hoặc so sánh căn nào, cứ nói cho Nera biết nhé! 😊"


def format_property_details_markdown(item: dict[str, Any]) -> str:
    location = ", ".join(filter(None, [item.get("address_line"), item.get("ward"), item.get("district"), item.get("province")]))
    desc = str(item.get("description") or "").strip()
    if len(desc) > 300:
        desc = desc[:300] + "..."

    lines = [
        f"### 🏠 {item.get('title', 'Thông tin Bất động sản')}\n",
        f"• **Giá niêm yết:** {_price_text(item.get('list_price'))}",
        f"• **Diện tích:** {item.get('area_sqm') or 'Chưa cập nhật'} m² ({item.get('bedrooms') or '—'} PN · {item.get('bathrooms') or '—'} WC)",
        f"• **Vị trí:** {location or 'Chưa cập nhật'}",
        f"• **Mã căn:** `{item.get('code') or item.get('id')}`",
    ]
    if desc:
        lines.append(f"\n**Mô tả nổi bật:**\n{desc}")

    lines.append("\nBạn có muốn Nera hỗ trợ **đặt lịch xem trực tiếp** căn này vào khung giờ nào không?")
    return "\n".join(lines)


async def format_intelligent_property_review(item: dict[str, Any], query: str) -> str:
    """Generate an intelligent, comprehensive AI review for the specific property."""
    try:
        llm = get_llm()._create_chat_model()
        sys_prompt = (
            "Bạn là Nera, chuyên gia tư vấn Bất động sản AI cao cấp, giọng văn thanh lịch, ấm áp và súc tích.\n"
            "Khách hàng đang xem chi tiết một bất động sản cụ thể và muốn bạn review nhanh, tư vấn về căn nhà này.\n\n"
            "Quy tắc trình bày chuẩn mực:\n"
            "- Trình bày mạch lạc, sử dụng các đoạn ngắn, xuống dòng thoáng mắt, dễ đọc trên khung chat nhỏ.\n"
            "- Sử dụng gạch đầu dòng bullet points rõ ràng cho các ý chính.\n"
            "- KHÔNG sử dụng ký tự tiêu đề thô (không dùng #, ##, ###), thay vào đó hãy dùng chữ in đậm **Tiêu đề** để giao diện nhỏ gọn gàng, đẹp mắt.\n"
            "- Cấu trúc phản hồi:\n"
            "  1. Tóm tắt nhanh: Tên căn, giá bán, diện tích, kết cấu và điểm ấn tượng nhất.\n"
            "  2. **Ưu điểm nổi bật:** 3-4 gạch đầu dòng ngắn gọn về vị trí, view, tiện ích, pháp lý và mức giá.\n"
            "  3. **Đánh giá & Khuyên dùng:** Căn này phù hợp nhất với nhu cầu nào (gia đình trẻ, mua ở lâu dài hay đầu tư cho thuê).\n"
            "  4. Lời kết thân thiện mời khách đặt lịch đi xem thực tế hoặc so sánh thêm."
        )
        context = {
            "customer_query": query,
            "property": {
                "title": item.get("title"),
                "price": _price_text(item.get("list_price")),
                "area_sqm": item.get("area_sqm"),
                "bedrooms": item.get("bedrooms"),
                "bathrooms": item.get("bathrooms"),
                "location": ", ".join(filter(None, [item.get("address_line"), item.get("ward"), item.get("district"), item.get("province")])),
                "legal_status": item.get("legal_status"),
                "orientation": item.get("orientation"),
                "description": str(item.get("description", ""))[:600],
            },
        }
        res = await llm.ainvoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=f"Thông tin căn nhà đang xem:\n{json.dumps(context, ensure_ascii=False, indent=2)}\n\nCâu hỏi/Yêu cầu của khách: {query}"),
        ])
        content = str(res.content).strip()
        if content:
            return content
    except Exception as exc:
        logger.warning(f"Error calling LLM for property review: {exc}")

    return format_property_details_markdown(item)


async def format_intelligent_comparison(items: list[dict[str, Any]], query: str) -> str:
    """Generate rich comparison table and direct LLM comparative analysis for user question."""
    # 1. Base Markdown Table
    table_lines = ["📊 **Bảng so sánh chi tiết giữa các bất động sản bạn quan tâm:**\n"]
    table_lines.append("| Tiêu chí | " + " | ".join(f"Căn {idx}: {it.get('title', '')[:25]}" for idx, it in enumerate(items, 1)) + " |")
    table_lines.append("|" + "---|" * (len(items) + 1))
    table_lines.append("| **Giá bán** | " + " | ".join(_price_text(it.get("list_price")) for it in items) + " |")
    table_lines.append("| **Diện tích** | " + " | ".join(f"{it.get('area_sqm') or '—'} m²" for it in items) + " |")
    table_lines.append("| **Kết cấu** | " + " | ".join(f"{it.get('bedrooms') or '—'} PN · {it.get('bathrooms') or '—'} WC" for it in items) + " |")
    table_lines.append("| **Vị trí** | " + " | ".join(", ".join(filter(None, [it.get("district"), it.get("province")])) for it in items) + " |")

    # 2. Call LLM for personalized comparative insights (e.g. "căn nào thoáng hơn", "gần trường hơn")
    try:
        llm = get_llm()._create_chat_model()
        sys_prompt = (
            "Bạn là Nera, chuyên gia tư vấn Bất động sản AI cao cấp, nhiệt tình, am hiểu và thấu hiểu khách hàng.\n"
            "Hãy so sánh các bất động sản và trả lời trực tiếp câu hỏi của khách hàng bằng giọng văn tự nhiên, ấm áp, mạch lạc và súc tích.\n\n"
            "Quy tắc định dạng:\n"
            "1. Mở đầu bằng một lời dẫn tự nhiên, thân thiện.\n"
            "2. Sử dụng bảng so sánh Markdown đẹp mắt (các cột: Tiêu chí, Căn 1, Căn 2...). Đảm bảo phân tích các hàng: Giá bán, Diện tích, Phòng ngủ / WC, Vị trí, Điểm nổi bật & Độ thoáng.\n"
            "3. Phần 'Đánh giá & Lời khuyên từ Nera': Trả lời trực diện vào câu hỏi của khách (ví dụ: căn nào thoáng hơn, ưu nhược điểm từng căn, phù hợp với ai) bằng giọng văn chuyên môn, khách quan.\n"
            "4. Tuyệt đối KHÔNG dùng các ký tự thừa như gạch nối rải rác, ký hiệu vụn vặt không cần thiết.\n"
            "5. Kết thúc bằng câu hỏi gợi ý nhẹ nhàng để khách đặt lịch đi xem thực tế."
        )
        context = {
            "customer_query": query,
            "properties": [
                {
                    "ordinal": idx,
                    "title": it.get("title"),
                    "price": _price_text(it.get("list_price")),
                    "area_sqm": it.get("area_sqm"),
                    "bedrooms": it.get("bedrooms"),
                    "bathrooms": it.get("bathrooms"),
                    "location": f"{it.get('address_line', '')}, {it.get('district', '')}, {it.get('province', '')}",
                    "description": str(it.get("description", ""))[:350],
                }
                for idx, it in enumerate(items, 1)
            ]
        }
        res = await llm.ainvoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=json.dumps(context, ensure_ascii=False))
        ])
        if res and res.content and len(res.content.strip()) > 30:
            return res.content.strip()
    except Exception as e:
        logger.warning(f"Intelligent comparison LLM failed: {e}. Using structured table.")

    table_lines.append("\nBạn có muốn Nera hỗ trợ đặt lịch đi xem thực tế căn nào trong số này không?")
    return "\n".join(table_lines)


def resolve_comparison_targets(query: str, pool: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Intelligently resolve which properties to compare from user natural query."""
    if not pool:
        return []
    q = query.lower()

    # 1. Relative positional phrases: "2 căn cuối", "hai căn cuối cùng", "căn cuối", "2 căn đầu", "3 căn đầu"
    if re.search(r"(?:2|hai)\s*căn\s*(?:cuối|sau)", q):
        return pool[-2:] if len(pool) >= 2 else pool
    if re.search(r"(?:3|ba)\s*căn\s*(?:cuối|sau)", q):
        return pool[-3:] if len(pool) >= 3 else pool
    if re.search(r"(?:2|hai)\s*căn\s*(?:đầu|trước)", q):
        return pool[:2]
    if re.search(r"(?:3|ba)\s*căn\s*(?:đầu|trước)", q):
        return pool[:3]
    if re.search(r"căn\s*(?:cuối|sau cùng)", q):
        return [pool[-1]]
    if re.search(r"căn\s*(?:đầu|thứ nhất)", q):
        return [pool[0]]

    # 2. Pair ordinals: "căn 1 và căn 2", "căn 4 và 5", "căn 1 với căn 3", "số 2 và 4"
    found_indices = []
    m_pair = re.search(r"căn\s*(?:số)?\s*(\d+)\s*(?:và|,|với)\s*(?:căn\s*(?:số)?)?\s*(\d+)", q)
    if m_pair:
        i1, i2 = int(m_pair.group(1)) - 1, int(m_pair.group(2)) - 1
        if 0 <= i1 < len(pool) and i1 not in found_indices:
            found_indices.append(i1)
        if 0 <= i2 < len(pool) and i2 not in found_indices:
            found_indices.append(i2)
    else:
        # Individual mentions: "căn 1", "căn 2", "căn 3"
        for m in re.finditer(r"(?:căn\s*(?:số|thứ)?|số)\s*(\d+)", q):
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(pool) and idx not in found_indices:
                found_indices.append(idx)

    if len(found_indices) >= 2:
        return [pool[i] for i in found_indices]

    # 3. Explicit quantities: "so sánh 2 căn", "so sánh 3 căn", "so sánh 4 căn"
    m_qty = re.search(r"so\s*sánh\s*(\d+)\s*căn", q)
    if m_qty:
        qty = int(m_qty.group(1))
        return pool[:qty]

    if re.search(r"so\s*sánh\s*hai\s*căn", q):
        return pool[:2]
    if re.search(r"so\s*sánh\s*ba\s*căn", q):
        return pool[:3]

    # 4. Default: take up to 2 items if pool has 2, else 3
    return pool[:2] if len(pool) == 2 else pool[:3]


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


async def answer_feature_question_on_properties(query: str, pool: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Answer direct questions about amenities/features for the current set of properties."""
    if not pool:
        return None

    try:
        llm = get_llm()._create_chat_model()
        sys_prompt = (
            "Bạn là Nera, chuyên gia tư vấn Bất động sản AI tận tâm, trung thực và am hiểu.\n"
            "Khách hàng đang hỏi một câu hỏi cụ thể về tiện ích/đặc điểm (như trường học, pháp lý/sổ đỏ, chỗ đỗ xe, ban công, độ thoáng, hướng...) "
            "đối với danh sách các bất động sản đang thảo luận.\n\n"
            "Hãy đọc kỹ thông tin và mô tả thực tế của các căn hộ dưới đây và trả lời trực tiếp cho khách hàng:\n"
            "1. Chỉ ra cụ thể căn số mấy đáp ứng tốt nhất yêu cầu của khách và giải thích chi tiết tại sao (dựa trên địa chỉ, mô tả tiện ích thực tế).\n"
            "2. Trình bày tự nhiên, ấm áp, mạch lạc theo từng đầu mục rõ ràng.\n"
            "3. Kết thúc bằng câu hỏi gợi ý xem chi tiết hoặc đặt lịch đi xem thực tế căn phù hợp."
        )
        context = {
            "customer_question": query,
            "properties": [
                {
                    "ordinal": idx,
                    "title": it.get("title"),
                    "price": _price_text(it.get("list_price")),
                    "area_sqm": it.get("area_sqm"),
                    "bedrooms": it.get("bedrooms"),
                    "location": f"{it.get('address_line', '')}, {it.get('district', '')}, {it.get('province', '')}",
                    "description": str(it.get("description", ""))[:400],
                }
                for idx, it in enumerate(pool, 1)
            ]
        }
        res = await llm.ainvoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=json.dumps(context, ensure_ascii=False))
        ])
        if res and res.content and len(res.content.strip()) > 30:
            res_text = res.content.strip()
            res_lower = res_text.lower()

            # Filter pool to only the properties specifically mentioned/recommended in the answer
            matched_props = []
            for idx, prop in enumerate(pool, 1):
                title = prop.get("title", "").lower()
                ordinal_patterns = [f"căn {idx}", f"căn số {idx}", f"căn thứ {idx}"]
                title_keywords = [w for w in title.split() if len(w) >= 3]

                is_matched = any(p in res_lower for p in ordinal_patterns)
                if not is_matched and len(title_keywords) >= 2:
                    # Match if key title phrase or at least 2 significant words are in the answer
                    is_matched = any(" ".join(title_keywords[i:i+2]) in res_lower for i in range(len(title_keywords) - 1))

                if is_matched and prop not in matched_props:
                    matched_props.append(prop)

            # If specific properties were matched, show ONLY them; otherwise show top 1
            final_selected = matched_props if matched_props else pool[:1]

            return {
                "response": res_text,
                "selected_properties": final_selected,
                "search_results": pool,
                "current_property_id": final_selected[0]["id"] if final_selected else None,
                "response_kind": "PROPERTY_ADVICE",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    "Xem chi tiết căn này",
                    "Đặt lịch xem nhà",
                    "So sánh với các căn khác",
                ],
            }
    except Exception as e:
        logger.warning(f"Feature QA LLM failed: {e}")
    return None


async def inventory_agent(state: AgentState) -> dict[str, Any]:
    """Inventory Agent node: handles searching, selecting, detailing, and comparing properties."""
    query = state.get("query", "")
    intent = state.get("intent")
    criteria = state.get("search_criteria", {})
    existing_properties = state.get("selected_properties", [])
    search_pool = state.get("search_results") or existing_properties
    soft_prefs = state.get("soft_preferences", [])
    current_prop_id = state.get("current_property_id")
    selected_idx = state.get("selected_property_index")

    # Step 0: Check if this is a feature question on existing search results
    q_low = query.lower()
    feature_patterns = [
        "có căn nào", "căn nào gần", "căn nào có", "căn nào view", "căn nào hướng", "căn nào tầng",
        "căn nào rẻ", "căn nào đẹp", "gần trường", "sổ đỏ", "sổ hồng", "ô tô", "đỗ xe", "để xe",
        "hầm", "gửi xe", "chính sách", "pháp lý", "thủ tục", "vay vốn", "ngân hàng", "tiện ích"
    ]
    if search_pool and any(p in q_low for p in feature_patterns) and not any(k in q_low for k in ["tìm thêm", "search", "lọc lại", "đổi sang"]):
        feature_ans = await answer_feature_question_on_properties(query, search_pool)
        if feature_ans:
            return feature_ans

    # Step 1: Handle COMPARE_PROPERTIES
    if intent == Intent.COMPARE_PROPERTIES:
        props = resolve_comparison_targets(query, search_pool)

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
            comparison_text = await format_intelligent_comparison(props, query)
            return {
                "selected_properties": props,
                "search_results": search_pool,
                "comparison_properties": props,
                "response": comparison_text,
                "response_kind": "PROPERTY_ADVICE",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    f"Chọn căn số {i}" for i in range(1, len(props) + 1)
                ] + ["Đặt lịch xem nhà"],
            }

    # Step 2: Handle PROPERTY_DETAILS (Evaluated before selection to answer questions on selected property!)
    if intent == Intent.PROPERTY_DETAILS:
        chosen = None
        q = query.lower()
        if re.search(r"căn\s*(?:cuối|sau cùng)", q) and search_pool:
            chosen = search_pool[-1]
        elif re.search(r"căn\s*(?:đầu|thứ nhất)", q) and search_pool:
            chosen = search_pool[0]
        else:
            m_ord = re.search(r"(?:căn\s*(?:số|thứ)?|số)\s*(\d+)", q)
            if m_ord and search_pool:
                idx = int(m_ord.group(1)) - 1
                if 0 <= idx < len(search_pool):
                    chosen = search_pool[idx]

        if not chosen and current_prop_id and search_pool:
            chosen = next((p for p in search_pool if p.get("id") == current_prop_id), None)
        if not chosen and search_pool:
            if selected_idx is not None and 0 <= selected_idx < len(search_pool):
                chosen = search_pool[selected_idx]
            else:
                chosen = search_pool[0]
        if not chosen and current_prop_id:
            loaded = await load_properties_by_ids([current_prop_id])
            if loaded:
                chosen = loaded[0]

        if chosen:
            detailed_response = await format_intelligent_property_review(chosen, query)
            return {
                "current_property_id": chosen["id"],
                "selected_properties": [chosen],
                "search_results": search_pool,
                "response": detailed_response,
                "response_kind": "PROPERTY_ADVICE",
                "phase": "PROPERTY_SELECTED",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    "Đặt lịch xem căn này",
                    "So sánh với các căn khác",
                    "Tìm căn khác",
                ],
            }

    # Step 3: Handle SELECT_PROPERTY
    if intent == Intent.SELECT_PROPERTY:
        if search_pool:
            if selected_idx is not None and 0 <= selected_idx < len(search_pool):
                chosen = search_pool[selected_idx]
            elif current_prop_id:
                chosen = next((p for p in search_pool if p.get("id") == current_prop_id), search_pool[0])
            else:
                chosen = search_pool[0]

            return {
                "current_property_id": chosen["id"],
                "selected_property_index": selected_idx if selected_idx is not None else 0,
                "selected_properties": [chosen],
                "search_results": search_pool,
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
            "search_results": [],
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
        "search_results": properties,
        "current_property_id": None,
        "selected_property_index": None,
        "response": format_search_results_markdown(properties, criteria, soft_prefs),
        "response_kind": "SEARCH_RESULTS",
        "phase": "SEARCH_RESULTS",
        "current_agent": AgentType.RESPOND,
        "suggested_actions": suggested_actions,
    }
