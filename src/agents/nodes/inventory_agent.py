"""Inventory Agent - Property Search, Details, and Comparison.

Queries real estate database with exact SQL constraints and formats grounded responses.
"""

import asyncio
import json
import logging
import re
from decimal import Decimal
from typing import Any
from uuid import UUID

from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload

from src.agents.state import AgentState, AgentType, Intent
from src.database.connection import get_session_context
from src.database.models import Property, PropertyKind, PropertyStatus
from src.services.chat_state_service import normalize_text
from src.services.geo_service import (
    GEO_NO_BASE_RESULTS_NOTE,
    GEO_NOT_CONFIGURED_NOTE,
    get_geo_service,
)
from src.services.llm import get_llm
from src.services.search_criteria_service import REGION_PROVINCES, extract_search_criteria
from src.utils.property_text import (
    clean_property_description,
    clean_property_title,
    get_search_variations,
    match_property_by_title,
)

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
        "title": clean_property_title(prop.title),
        "description": clean_property_description(prop.description),
        "status": prop.status.value if prop.status else None,
        "address_line": prop.address_line,
        "ward": prop.ward,
        "district": prop.district,
        "province": prop.province,
        "latitude": _num(prop.latitude),
        "longitude": _num(prop.longitude),
        "area_sqm": _num(prop.area_sqm),
        "bedrooms": prop.bedrooms,
        "bathrooms": prop.bathrooms,
        "floor_number": prop.floor_number,
        "orientation": prop.orientation,
        "legal_status": prop.legal_status,
        "list_price": _num(prop.list_price),
        "currency": prop.currency,
        "features": prop.features or {},
        "media": media_payload,
        "image": media_payload[0]["url"] if media_payload else None,
    }


def _interleave_properties_by_province(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Distribute properties evenly across provinces in a broad region search."""
    by_prov: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        prov = str(item.get("province") or "Khác")
        by_prov.setdefault(prov, []).append(item)

    result: list[dict[str, Any]] = []
    prov_lists = list(by_prov.values())
    idx = 0
    while len(result) < limit and any(idx < len(lst) for lst in prov_lists):
        for lst in prov_lists:
            if idx < len(lst) and len(result) < limit:
                result.append(lst[idx])
        idx += 1
    return result


async def query_properties_from_db(
    criteria: dict[str, Any],
    limit: int = 20,
    exclude_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Execute dynamic criteria search against PostgreSQL with relationship eager-loading."""
    effective_limit = criteria.get("limit") or limit
    async with get_session_context() as session:
        filters = [Property.status == PropertyStatus.AVAILABLE]

        if exclude_ids:
            parsed_excludes = []
            for raw in exclude_ids:
                try:
                    parsed_excludes.append(UUID(str(raw)))
                except (ValueError, TypeError):
                    continue
            if parsed_excludes:
                filters.append(Property.id.notin_(parsed_excludes))

        area_target = criteria.get("area_or_ward") or criteria.get("ward")
        district = criteria.get("district")
        province = criteria.get("province")
        region = criteria.get("region")
        property_kind = criteria.get("property_kind")

        # Resolve region if province holds a region name
        if province:
            norm_prov = normalize_text(str(province)).lower()
            if "mien bac" in norm_prov or "bac bo" in norm_prov:
                region = "Miền Bắc"
                province = None
            elif "mien trung" in norm_prov or "trung bo" in norm_prov:
                region = "Miền Trung"
                province = None
            elif "mien nam" in norm_prov or "nam bo" in norm_prov:
                region = "Miền Nam"
                province = None

        if area_target:
            area_vars = get_search_variations(area_target)
            area_filters = []
            for v in area_vars:
                area_filters.extend([
                    Property.ward.ilike(f"%{v}%"),
                    Property.address_line.ilike(f"%{v}%"),
                    Property.title.ilike(f"%{v}%"),
                ])
            filters.append(or_(*area_filters))

        if district:
            dist_vars = get_search_variations(district)
            filters.append(or_(*[Property.district.ilike(f"%{v}%") for v in dist_vars]))
        elif province:
            prov_vars = get_search_variations(province)
            filters.append(or_(*[Property.province.ilike(f"%{v}%") for v in prov_vars]))
        elif region:
            matched_region_provinces = None
            norm_reg = normalize_text(str(region)).lower()
            if "bac" in norm_reg:
                matched_region_provinces = REGION_PROVINCES.get("Miền Bắc")
            elif "trung" in norm_reg:
                matched_region_provinces = REGION_PROVINCES.get("Miền Trung")
            elif "nam" in norm_reg:
                matched_region_provinces = REGION_PROVINCES.get("Miền Nam")

            if matched_region_provinces:
                reg_filters = []
                for p in matched_region_provinces:
                    for pv in get_search_variations(p):
                        reg_filters.append(Property.province.ilike(f"%{pv}%"))
                if reg_filters:
                    filters.append(or_(*reg_filters))

        if property_kind:
            try:
                filters.append(Property.property_kind == PropertyKind(str(property_kind)))
            except ValueError:
                pass

        if criteria.get("min_price") is not None:
            filters.append(Property.list_price >= criteria["min_price"])
        if criteria.get("max_price") is not None:
            filters.append(Property.list_price <= criteria["max_price"])
        if criteria.get("min_bedrooms") is not None and criteria["min_bedrooms"] > 0:
            filters.append(Property.bedrooms >= criteria["min_bedrooms"])
        if criteria.get("max_bedrooms") is not None and criteria["max_bedrooms"] > 0:
            filters.append(Property.bedrooms <= criteria["max_bedrooms"])
        if criteria.get("min_bathrooms") is not None and criteria["min_bathrooms"] > 0:
            filters.append(Property.bathrooms >= criteria["min_bathrooms"])
        if criteria.get("min_area") is not None and criteria["min_area"] > 0:
            filters.append(Property.area_sqm >= criteria["min_area"])
        if criteria.get("min_floor") is not None:
            filters.append(Property.floor_number >= criteria["min_floor"])
        if criteria.get("max_floor") is not None:
            filters.append(Property.floor_number <= criteria["max_floor"])
        if criteria.get("orientation"):
            filters.append(Property.orientation.ilike(f"%{criteria['orientation']}%"))
        if criteria.get("legal_status"):
            filters.append(Property.legal_status.ilike(f"%{criteria['legal_status']}%"))
        if criteria.get("transaction_type"):
            filters.append(Property.features["listing_type"].astext == criteria["transaction_type"])
        if criteria.get("furniture_status"):
            filters.append(
                Property.features["furniture_status"].astext.ilike(
                    f"%{criteria['furniture_status']}%"
                )
            )

        is_broad_region_search = bool(region and not province and not district and not area_target)
        query_limit = 100 if is_broad_region_search else effective_limit

        order_clauses = []
        if criteria.get("max_price") is not None and criteria.get("min_price") is None:
            order_clauses.append(func.abs(Property.list_price - criteria["max_price"]).asc())
        elif criteria.get("min_price") is not None and criteria.get("max_price") is not None:
            mid_price = (criteria["min_price"] + criteria["max_price"]) / 2
            order_clauses.append(func.abs(Property.list_price - mid_price).asc())
        elif criteria.get("min_price") is not None:
            order_clauses.append(Property.list_price.asc())

        order_clauses.append(Property.published_at.desc().nullslast())

        stmt = (
            select(Property)
            .options(selectinload(Property.media))
            .where(*filters)
            .order_by(*order_clauses)
            .limit(query_limit)
        )
        rows = (await session.execute(stmt)).scalars().all()
        items = [serialize_property_item(r) for r in rows]

        if is_broad_region_search:
            return _interleave_properties_by_province(items, limit=effective_limit)

        return items


async def count_rental_listings() -> int:
    """Number of listings marked for rent, ignoring every other criterion.

    A zero here means Nera has no rentals at all, which is a different answer to
    the customer than "none matched your budget" and must not be blurred into it.
    """
    async with get_session_context() as session:
        stmt = select(func.count()).select_from(Property).where(
            Property.features["listing_type"].astext == "RENT"
        )
        return int((await session.execute(stmt)).scalar() or 0)


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
    loc_parts = []
    area_target = (criteria.get("area_or_ward") or criteria.get("ward") or "").strip()
    district = (criteria.get("district") or "").strip()
    province = (criteria.get("province") or "").strip()
    region = (criteria.get("region") or "").strip()

    def _norm(s: str) -> str:
        return normalize_text(s).lower().strip()

    if province:
        norm_p = _norm(province)
        if "mien bac" in norm_p or "bac bo" in norm_p:
            region = "Miền Bắc"
            province = ""
        elif "mien trung" in norm_p or "trung bo" in norm_p:
            region = "Miền Trung"
            province = ""
        elif "mien nam" in norm_p or "nam bo" in norm_p:
            region = "Miền Nam"
            province = ""

    if area_target:
        norm_area = _norm(area_target)
        if (
            (district and norm_area == _norm(district))
            or (province and norm_area == _norm(province))
            or (region and norm_area == _norm(region))
            or norm_area in {"ha noi", "ho chi minh", "da nang", "mien bac", "mien trung", "mien nam"}
        ):
            area_target = ""

    if area_target:
        loc_parts.append(area_target)
    if district:
        loc_parts.append(district)
    elif province:
        loc_parts.append(province)
    elif region:
        loc_parts.append(region)

    seen = set()
    unique_loc = []
    for lp in loc_parts:
        nlp = _norm(lp)
        if lp and nlp not in seen:
            seen.add(nlp)
            unique_loc.append(lp)

    if unique_loc:
        parts.append(", ".join(unique_loc))

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
    if criteria.get("min_bedrooms") is not None and criteria["min_bedrooms"] > 0:
        if criteria.get("max_bedrooms") == criteria["min_bedrooms"]:
            parts.append(f"{criteria['min_bedrooms']} phòng ngủ")
        else:
            parts.append(f"{criteria['min_bedrooms']}+ phòng ngủ")
    elif criteria.get("max_bedrooms") is not None and criteria["max_bedrooms"] > 0:
        parts.append(f"tối đa {criteria['max_bedrooms']} phòng ngủ")
    if criteria.get("min_area") is not None and criteria["min_area"] > 0:
        area_val = _num(criteria["min_area"])
        if area_val is not None:
            parts.append(f"từ {area_val:g} m²")
    if criteria.get("transaction_type") == "RENT":
        parts.append("cho thuê")
    elif criteria.get("transaction_type") == "SALE":
        parts.append("mua bán")
    if criteria.get("orientation"):
        parts.append(f"hướng {criteria['orientation']}")
    if criteria.get("legal_status"):
        parts.append(str(criteria["legal_status"]))
    if criteria.get("min_floor") is not None and criteria.get("max_floor") == criteria.get("min_floor"):
        parts.append(f"tầng {criteria['min_floor']}")
    elif criteria.get("min_floor") is not None or criteria.get("max_floor") is not None:
        parts.append(f"tầng {criteria.get('min_floor', '—')}–{criteria.get('max_floor', '—')}")

    return ", ".join(parts)


def format_search_results_markdown(
    items: list[dict[str, Any]],
    criteria: dict[str, Any],
    soft_prefs: list[str],
    affordability_note: str | None = None,
) -> str:
    summary = format_criteria_summary(criteria)
    total_count = len(items)
    requested_limit = criteria.get("limit")

    if requested_limit and requested_limit < total_count:
        display_items = items[:requested_limit]
    elif not requested_limit and total_count > 5:
        display_items = items[:5]
    else:
        display_items = items

    intro = f"Nera đã tìm thấy **{total_count} bất động sản** phù hợp nhất"
    if summary:
        intro += f" với tiêu chí **{summary}**"
    if not requested_limit and total_count > 5:
        intro += " cho bạn (dưới đây là 5 căn nổi bật nhất, bạn có thể bấm xem thêm ở danh sách bên dưới):"
    else:
        intro += " cho bạn:"

    blocks = []
    for index, item in enumerate(display_items, 1):
        location = ", ".join(filter(None, [item.get("district"), item.get("province")])) or "Chưa cập nhật"
        is_rental = criteria.get("transaction_type") == "RENT"
        price = _price_text(item.get("list_price")) + ("/tháng" if is_rental else "")
        area_num = _num(item.get("area_sqm"))
        area = f"{area_num:g} m²" if area_num is not None else ""
        beds = f"{item.get('bedrooms')} PN" if item.get("bedrooms") is not None else ""
        specs = " · ".join(filter(None, [price, area, beds, location]))
        distance = item.get("distance_evidence") or {}
        if distance:
            specs += (
                f"\n🚗 {distance.get('distance_km')} km · "
                f"{distance.get('duration_minutes')} phút đến {distance.get('destination')} "
                f"({distance.get('travel_mode')})"
            )
        nearby = item.get("nearby_evidence") or []
        if nearby:
            nearest = nearby[0]
            specs += f"\n📍 Gần {nearest.get('name')} (~{nearest.get('straight_line_km')} km đường chim bay)"
        blocks.append(f"**{index}. {item.get('title', 'Bất động sản')}**\n{specs}")

    body = "\n\n".join(blocks)
    note = f"\n\n*(Đã cân nhắc thêm: {', '.join(soft_prefs)})*" if soft_prefs else ""

    rental_note = (
        "\n\n*Giá trên là giá thuê theo tháng. Tiền cọc, phí quản lý và điều kiện thuê "
        "cần được xác nhận lại với chủ tin.*"
        if criteria.get("transaction_type") == "RENT"
        else ""
    )

    # When the ceiling came from stated income, show the working before the list.
    # A price range the customer cannot check is worse than no range at all.
    prefix = f"{affordability_note}\n\n---\n\n" if affordability_note else ""

    closing = "Bạn muốn xem chi tiết hoặc so sánh căn nào, cứ nói cho Nera biết nhé! 😊"
    if affordability_note:
        closing = (
            "Nếu bạn cho Nera biết số vốn tự có, Nera tính lại tầm giá sát hơn. "
            "Hoặc bạn muốn xem chi tiết căn nào, cứ nói nhé! 😊"
        )

    return f"{prefix}{intro}\n\n{body}{note}{rental_note}\n\n{closing}"


async def format_intelligent_search_results(
    items: list[dict[str, Any]],
    criteria: dict[str, Any],
    soft_prefs: list[str],
    query: str,
    affordability_note: str | None = None,
    is_resume: bool = False,
    memory_summary: str | None = None,
) -> str:
    """Generate a dynamic, natural, and insightful property introduction using LLM."""
    if not items:
        return format_search_results_markdown(items, criteria, soft_prefs, affordability_note)

    try:
        llm = get_llm()._create_chat_model()
        sys_prompt = (
            "Bạn là Nera – Trợ lý AI kiêm chuyên viên tư vấn bất động sản cao cấp hàng đầu, phong thái tự nhiên, thông minh, ấm áp và súc tích.\n"
            "Bạn vừa tìm được danh sách các bất động sản phù hợp từ kho dữ liệu có thật của hệ thống.\n\n"
            "Quy tắc phản hồi chuẩn mực:\n"
            "- Lời mở đầu & Phân tích mức giá: Tuân thủ nghiêm ngặt trường `price_analysis` (nếu có):\n"
            "  + Nếu có căn đúng mức giá yêu cầu (hoặc sát trong khoảng 2-5%): Nêu rõ có bao nhiêu căn đúng giá hoặc sát nhất với ngân sách khách hỏi. Nếu có hiển thị thêm các căn rẻ hơn ở phía sau, hãy giới thiệu như phương án tham khảo thêm, tuyệt đối không gộp chung coi như tất cả đều là mức giá đó.\n"
            "  + Nếu không có căn nào đúng giá: Thành thật nêu rõ 'Hiện tại trong kho dữ liệu chưa có căn đúng chính xác [Giá], Nera xin gợi ý các căn có mức giá gần nhất hiện có ([Mức giá])' và hỏi khách có muốn xem phân khúc trên hay dưới mức giá này không.\n"
            "- Danh sách các căn nổi bật: Trình bày rõ ràng các căn đầu tiên theo format đánh số:\n"
            "  **1. [Tên BĐS]**\n"
            "  [Giá] · [Diện tích] m² · [Số PN] PN · [Địa chỉ/Quận, Tỉnh/TP]\n"
            "  *(Gợi ý/Điểm cộng: 1 câu nhận xét ngắn gọn vì sao căn này đáng chú ý đối với tiêu chí của khách)*\n"
            "- Tuyệt đối GIỮ NGUYÊN các thông số thực tế (giá niêm yết, diện tích, số phòng ngủ, vị trí) từ dữ liệu cung cấp, KHÔNG được bịa đặt số liệu khác.\n"
            "- Lời kết: Thân thiện, tự nhiên mời khách bấm chọn căn để xem chi tiết, so sánh hoặc đặt lịch xem nhà."
        )

        display_limit = criteria.get("limit") or 5
        candidate_items = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "price": _price_text(p.get("list_price")),
                "area_sqm": p.get("area_sqm"),
                "bedrooms": p.get("bedrooms"),
                "location": ", ".join(filter(None, [p.get("district"), p.get("province")])),
                "features": p.get("features") or {},
                "description": str(p.get("description") or "")[:200],
            }
            for p in items[:display_limit]
        ]

        target_price = criteria.get("target_price")
        price_analysis: dict[str, Any] | None = None

        if target_price and items:
            diffs = [
                abs(float(p.get("list_price") or 0) - float(target_price)) / float(target_price)
                for p in items[:display_limit]
                if p.get("list_price")
            ]
            has_exact = any(d <= 0.01 for d in diffs)
            has_close = any(d <= 0.05 for d in diffs)
            min_diff = min(diffs) if diffs else 0
            if has_exact or has_close:
                exact_count = sum(1 for d in diffs if d <= 0.01)
                close_count = sum(1 for d in diffs if d <= 0.05)
                price_analysis = {
                    "status": "EXACT_OR_CLOSE_MATCH",
                    "exact_matches_count": exact_count,
                    "close_matches_count": close_count,
                    "target_price": _price_text(target_price),
                    "instruction": (
                        f"Có {exact_count} căn đúng chính xác và {close_count} căn rất sát "
                        f"(trong khoảng chênh lệch dưới 5%) với mức giá {_price_text(target_price)} khách hỏi. "
                        f"Hãy nêu rõ các căn đúng/sát giá này. Các căn có mức giá thấp hơn ở sau "
                        f"chỉ là phương án tham khảo thêm trong tầm ngân sách, không giới thiệu chung là đúng {_price_text(target_price)}."
                    ),
                }
            elif min_diff > 0.08:
                nearest_price = items[0].get("list_price")
                price_analysis = {
                    "status": "NO_EXACT_MATCH",
                    "target_price": _price_text(target_price),
                    "nearest_price": _price_text(nearest_price) if nearest_price else "—",
                    "instruction": (
                        f"Trong kho dữ liệu hiện tại KHÔNG CÓ căn nào đúng chính xác mức giá {_price_text(target_price)}. "
                        f"Căn có giá gần nhất hiện có là {_price_text(nearest_price)}. "
                        f"Hãy nêu rõ ràng điều này cho khách biết rằng Nera chọn lọc các căn có mức giá gần nhất hiện có, "
                        f"và hỏi khách có muốn xem các căn ở phân khúc trên hay dưới {_price_text(target_price)} không."
                    ),
                }
        elif criteria.get("max_price") and items:
            max_p = criteria["max_price"]
            price_analysis = {
                "status": "BUDGET_CEILING",
                "max_price": _price_text(max_p),
                "instruction": (
                    f"Khách hàng tìm kiếm bất động sản trong tầm ngân sách DƯỚI / TỐI ĐA {_price_text(max_p)}. "
                    f"Tất cả các căn hộ bên dưới đều thỏa mãn hoàn hảo điều kiện ngân sách này. "
                    f"TUYỆT ĐỐI KHÔNG NÓI 'chưa có căn đúng chính xác {_price_text(max_p)}' hay 'không có căn đúng {_price_text(max_p)}', "
                    f"bởi vì khách hàng chỉ yêu cầu trần ngân sách dưới {_price_text(max_p)} chứ không đòi hỏi đúng chính xác {_price_text(max_p)}. "
                    f"Hãy giới thiệu tự nhiên các căn hộ nổi bật nhất trong tầm ngân sách dưới {_price_text(max_p)}."
                ),
            }

        payload = {
            "customer_query": query,
            "search_criteria": criteria,
            "soft_preferences": soft_prefs,
            "total_found": len(items),
            "is_resume_user": is_resume,
            "memory_summary": memory_summary,
            "price_analysis": price_analysis,
            "top_properties": candidate_items,
        }
        if affordability_note:
            payload["affordability_calculation"] = affordability_note

        res = await llm.ainvoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(
                content=f"Dữ liệu tìm kiếm từ hệ thống:\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
                f"Hãy phản hồi cho khách hàng thật xuất sắc, tự nhiên và chuyên nghiệp:"
            ),
        ])
        content = str(res.content).strip()
        if content and len(content) > 50:
            prefix = f"{affordability_note}\n\n---\n\n" if affordability_note and affordability_note not in content else ""
            return f"{prefix}{content}"
    except Exception as exc:
        logger.warning(f"Intelligent search formatting failed: {exc}. Using deterministic fallback.")

    return format_search_results_markdown(items, criteria, soft_prefs, affordability_note)


def format_property_details_markdown(
    item: dict[str, Any],
    *,
    include_description: bool = True,
) -> str:
    location = ", ".join(filter(None, [item.get("address_line"), item.get("ward"), item.get("district"), item.get("province")]))
    desc = clean_property_description(item.get("description"), max_chars=300) or ""

    lines = [
        f"### 🏠 {item.get('title', 'Thông tin Bất động sản')}\n",
        f"• **Giá niêm yết:** {_price_text(item.get('list_price'))}",
        f"• **Diện tích:** {item.get('area_sqm') or 'Chưa cập nhật'} m² ({item.get('bedrooms') or '—'} PN · {item.get('bathrooms') or '—'} WC)",
        f"• **Vị trí:** {location or 'Chưa cập nhật'}",
        f"• **Mã căn:** `{item.get('code') or item.get('id')}`",
    ]
    if desc and include_description:
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
                    "floor_number": it.get("floor_number"),
                    "orientation": it.get("orientation"),
                    "legal_status": it.get("legal_status"),
                    "features": it.get("features", {}),
                    "location": f"{it.get('address_line', '')}, {it.get('district', '')}, {it.get('province', '')}",
                    "description": str(it.get("description", ""))[:350],
                }
                for idx, it in enumerate(items, 1)
            ]
        }
        res = await asyncio.wait_for(
            llm.ainvoke([
                SystemMessage(content=sys_prompt),
                HumanMessage(content=json.dumps(context, ensure_ascii=False)),
            ]),
            timeout=6,
        )
        if res and res.content and len(res.content.strip()) > 30:
            return res.content.strip()
    except Exception as e:
        logger.warning(f"Intelligent comparison LLM failed: {e}. Using structured table.")

    table_lines.append("\nBạn có muốn Nera hỗ trợ đặt lịch đi xem thực tế căn nào trong số này không?")
    return "\n".join(table_lines)


def resolve_comparison_targets(
    query: str,
    pool: list[dict[str, Any]],
    current_property_id: str | None = None,
) -> list[dict[str, Any]]:
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

    if len(found_indices) == 1 and current_property_id:
        current_idx = next(
            (idx for idx, item in enumerate(pool) if item.get("id") == current_property_id),
            None,
        )
        if current_idx is not None and current_idx not in found_indices:
            found_indices.insert(0, current_idx)

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
            "Bạn là Nera, chuyên gia tư vấn Bất động sản AI tận tâm, trung thực và súc tích.\n"
            "Khách hàng đang hỏi một câu hỏi cụ thể về đặc điểm/tiện ích/số phòng ngủ/diện tích/giá của danh sách các bất động sản đang thảo luận (ví dụ: 'căn nào trên 2 phòng ngủ ko', 'căn nào có chỗ đỗ ô tô', 'căn nào gần trường').\n\n"
            "Hãy đọc kỹ thông tin các căn dưới đây và trả lời trực tiếp cho khách hàng:\n"
            "1. Trả lời thẳng vào câu hỏi ngay ở đầu câu (ví dụ: 'Trong 3 căn đang xem, chỉ có Căn 2: Feliz Home 297 Hoàng Mai là có 3 phòng ngủ (114 m²)...').\n"
            "2. Nêu rõ lý do ngắn gọn vì sao căn đó phù hợp và vì sao các căn khác chưa phù hợp.\n"
            "3. Tuyệt đối KHÔNG vẽ bảng so sánh Markdown (vì khách chỉ hỏi 1 câu hỏi cụ thể, không yêu cầu so sánh).\n"
            "4. Kết thúc bằng câu gợi ý ngắn gọn để khách xem chi tiết hoặc đặt lịch đi xem thực tế."
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
                    "bathrooms": it.get("bathrooms"),
                    "floor_number": it.get("floor_number"),
                    "orientation": it.get("orientation"),
                    "legal_status": it.get("legal_status"),
                    "features": it.get("features", {}),
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
                ordinal_patterns = [
                    f"căn {idx}", f"căn số {idx}", f"căn thứ {idx}",
                    f"căn hộ {idx}", f"căn hộ số {idx}", f"bất động sản {idx}"
                ]
                prop_code = str(prop.get("code") or "").lower()

                is_matched = any(p in res_lower for p in ordinal_patterns)
                if not is_matched and prop_code and len(prop_code) >= 3 and prop_code in res_lower:
                    is_matched = True

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
    is_explicit_compare = bool(re.search(r"\b(so sanh|doi chieu|lap bang so sanh)\b", q_low))
    det_crit, det_grps = extract_search_criteria(query)
    has_search_entities = bool(
        "location" in det_grps
        or "budget" in det_grps
        or "property_kind" in det_crit
        or "min_bedrooms" in det_crit
        or "min_area" in det_crit
        or "limit" in det_crit
        or any(key in det_crit for key in (
            "transaction_type", "orientation", "legal_status", "furniture_status",
            "min_floor", "max_floor",
        ))
        or state.get("nearby_categories")
        or state.get("commute_landmark")
        or re.search(r"\b(tim|tim kiem|mua|xem|loc|kiem|co can nao o|co nha nao o|co can nao duoi|co can nao tren)\b", q_low)
    )

    feature_patterns = [
        "căn nào", "có căn nào", "căn mấy", "căn số mấy", "căn thứ mấy",
        "phòng ngủ", "pn", "diện tích", "m2", "m²", "rẻ nhất", "đắt nhất", "rẻ hơn",
        "gần trường", "sổ đỏ", "sổ hồng", "ô tô", "đỗ xe", "để xe", "ban công", "view",
        "hướng", "tầng", "hầm", "gửi xe", "chính sách", "pháp lý", "thủ tục", "vay vốn", "ngân hàng", "tiện ích"
    ]
    if search_pool and not is_explicit_compare and not has_search_entities and any(p in q_low for p in feature_patterns) and not any(k in q_low for k in ["tìm thêm", "search", "lọc lại", "đổi sang"]):
        feature_ans = await answer_feature_question_on_properties(query, search_pool)
        if feature_ans:
            return feature_ans

    # Step 1: Handle COMPARE_PROPERTIES
    if intent == Intent.COMPARE_PROPERTIES:
        props = resolve_comparison_targets(query, search_pool, current_prop_id)

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

        if not chosen and search_pool:
            matched_idx, matched_prop = match_property_by_title(query, search_pool)
            if matched_prop:
                chosen = matched_prop
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
            geo_note = None
            detail_geo_requested = bool(
                state.get("commute_landmark")
                or state.get("nearby_categories")
                or state.get("max_commute_km") is not None
                or state.get("max_commute_minutes") is not None
            )
            if detail_geo_requested:
                geo_result = await get_geo_service().enrich_and_filter(
                    [chosen],
                    destination=state.get("commute_landmark"),
                    destination_coordinates=(
                        (state["user_location"]["latitude"], state["user_location"]["longitude"])
                        if state.get("user_location") else None
                    ),
                    travel_mode=state.get("travel_mode", "DRIVE"),
                    nearby_categories=state.get("nearby_categories", []),
                )
                if geo_result.properties:
                    chosen = geo_result.properties[0]
                geo_note = geo_result.note
            if detail_geo_requested:
                # Geo answers must be deterministic. Listing descriptions and an
                # unconstrained LLM may contain unverified "near" or km claims.
                detailed_response = format_property_details_markdown(
                    chosen,
                    include_description=False,
                )
            else:
                detailed_response = await format_intelligent_property_review(chosen, query)
            if chosen.get("distance_evidence"):
                evidence = chosen["distance_evidence"]
                detailed_response = (
                    f"**Khoảng cách đã xác minh:** {evidence['distance_km']} km, khoảng "
                    f"{evidence['duration_minutes']} phút đến {evidence['destination']} "
                    f"({evidence['travel_mode']}, {evidence['provider']}).\n\n"
                    + detailed_response
                )
            elif geo_note:
                detailed_response = f"⚠️ {geo_note}\n\n{detailed_response}"
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
            matched_idx, matched_prop = match_property_by_title(query, search_pool)
            if matched_prop:
                chosen = matched_prop
                selected_idx = matched_idx
            elif selected_idx is not None and 0 <= selected_idx < len(search_pool):
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
    q_norm = normalize_text(query)
    if (
        re.search(r"\b(thay doi nhu cau|doi nhu cau|nhu cau moi|xoa tieu chi|muon thay doi)\b", q_norm)
        and not det_crit
    ):
        return {
            "response": "Dạ vâng! Nera đã làm mới yêu cầu tìm kiếm cho bạn.\n\nBạn hãy chia sẻ nhu cầu mới nhé:\n- **Khu vực bạn muốn tìm** (ví dụ: Cầu Giấy, Nam Từ Liêm, Quận 7...)\n- **Khoảng ngân sách mong muốn** (ví dụ: dưới 5 tỷ, 15-20 triệu/tháng...)\n- **Số phòng ngủ & Loại nhà** (ví dụ: Căn hộ 2PN, Nhà phố...)",
            "response_kind": "ASK_CRITERIA",
            "phase": "IDLE",
            "search_criteria": {},
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                "Căn hộ Cầu Giấy dưới 5 tỷ",
                "Nhà riêng Thanh Xuân 3PN",
                "Chung cư Nam Từ Liêm 2 phòng ngủ",
            ],
        }

    has_core_filters = bool(
        criteria.get("district")
        or criteria.get("province")
        or criteria.get("region")
        or criteria.get("area_or_ward")
        or criteria.get("ward")
        or criteria.get("property_kind")
        or criteria.get("min_price")
        or criteria.get("max_price")
        or criteria.get("transaction_type")
        or criteria.get("orientation")
        or criteria.get("legal_status")
        or criteria.get("furniture_status")
        or criteria.get("min_floor") is not None
        or criteria.get("max_floor") is not None
        or state.get("commute_landmark")
        or state.get("user_location")
        or state.get("nearby_categories")
    )

    is_resume = bool(re.search(
        r"\b(tiep tuc|nhu cau cu|so thich da luu|nhu lan truoc|nhu cu|tim lai|theo tieu chi cu|tiep tuc hanh trinh|tiep tuc tim kiem)\b",
        q_norm,
    )) or bool(state.get("is_resume_search"))

    if not has_core_filters:
        mem_sum = state.get("memory_summary")
        if mem_sum and is_resume:
            return {
                "response": f"Chào bạn quay lại! Nera nhớ lần trước bạn quan tâm: **{mem_sum}**.\n\nHiện tại chưa có đủ thông số để lọc chính xác, bạn muốn tìm ở khu vực nào hay mức giá cụ thể bao nhiêu để Nera tìm ngay cho bạn nhé?",
                "response_kind": "ASK_CRITERIA",
                "phase": "IDLE",
                "search_criteria": criteria,
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    f"Tìm quanh {mem_sum}",
                    "Thay đổi nhu cầu tìm kiếm",
                ],
            }
        return {
            "response": "Để mình tìm được căn hộ/nhà đất ưng ý nhất cho bạn, bạn chia sẻ thêm một vài thông tin nhé:\n- **Khu vực mong muốn** (ví dụ: Quận 7, Cầu Giấy, Bình Thạnh...)\n- **Khoảng ngân sách** (ví dụ: dưới 5 tỷ, 15-20 triệu/tháng...)\n- **Loại hình & số phòng ngủ** (ví dụ: căn hộ 2PN, nhà phố...)",
            "response_kind": "ASK_CRITERIA",
            "phase": "IDLE",
            "search_criteria": {},
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                "Căn hộ Quận 7 dưới 5 tỷ",
                "Nhà riêng Cầu Giấy 3 phòng ngủ",
                "Chung cư 2PN gần trung tâm",
            ],
        }

    is_asking_other = bool(re.search(
        r"\b(cai khac|can khac|nha khac|xem them|con khac|co can nao khac|con cai gi khac|con can gi khac|khac khong|khac ko|khac di|doi can khac)\b",
        q_norm,
    ))

    exclude_ids = []
    if is_asking_other:
        exclude_ids = [p["id"] for p in existing_properties if p.get("id")]
        if not exclude_ids and search_pool:
            exclude_ids = [p["id"] for p in search_pool if p.get("id")]

    search_limit = criteria.get("limit") or 20
    properties = await query_properties_from_db(
        criteria,
        limit=search_limit,
        exclude_ids=exclude_ids if is_asking_other else None,
    )

    geo_requested = bool(
        state.get("commute_landmark")
        or state.get("nearby_categories")
        or state.get("max_commute_km") is not None
        or state.get("max_commute_minutes") is not None
    )
    geo_note = None
    if geo_requested:
        geo_service = get_geo_service()
        if not properties:
            geo_note = (
                GEO_NOT_CONFIGURED_NOTE
                if not geo_service.configured
                else GEO_NO_BASE_RESULTS_NOTE
            )
        else:
            geo_result = await geo_service.enrich_and_filter(
                properties,
                destination=state.get("commute_landmark"),
                destination_coordinates=(
                    (state["user_location"]["latitude"], state["user_location"]["longitude"])
                    if state.get("user_location") else None
                ),
                travel_mode=state.get("travel_mode", "DRIVE"),
                max_km=state.get("max_commute_km"),
                max_minutes=state.get("max_commute_minutes"),
                nearby_categories=state.get("nearby_categories", []),
            )
            properties = geo_result.properties
            geo_note = geo_result.note

    if is_asking_other and not properties:
        summary = format_criteria_summary(criteria)
        return {
            "selected_properties": existing_properties,
            "search_results": search_pool,
            "response": f"Hiện tại trong kho dữ liệu với tiêu chí **{summary or 'hiện tại'}** chỉ có các căn đã giới thiệu ở trên.\n\n💡 **Gợi ý mở rộng:**\n- Thử nới rộng ngân sách hoặc mở rộng sang các quận lân cận\n- Thay đổi số phòng ngủ hoặc loại hình nhà\n\nBạn có muốn Nera tìm kiếm mở rộng sang khu vực lân cận không?",
            "response_kind": "PROPERTY_LIST",
            "phase": "PROPERTY_SELECTED",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                "Mở rộng sang quận lân cận",
                "Tăng khoảng ngân sách",
                "Thay đổi nhu cầu",
            ],
        }

    # Check if returning user continuation
    if is_resume and properties:
        response_msg = await format_intelligent_search_results(
            properties,
            criteria,
            soft_prefs,
            query,
            affordability_note=state.get("affordability_note"),
            is_resume=True,
            memory_summary=state.get("memory_summary"),
        )
        display_items = properties[:5] if len(properties) > 5 else properties
        return {
            "selected_properties": properties,
            "search_results": properties,
            "current_property_id": None,
            "selected_property_index": None,
            "response": response_msg,
            "response_kind": "PROPERTY_LIST",
            "phase": "PROPERTY_SELECTED",
            "current_agent": AgentType.RESPOND,
            "suggested_actions": [
                f"Chọn căn số {i}" for i in range(1, min(len(display_items) + 1, 4))
            ] + ["Thay đổi nhu cầu"],
        }

    if not properties:
        summary = format_criteria_summary(criteria)
        if geo_requested and not geo_note:
            geo_note = (
                "Đã xác minh bằng Google Maps nhưng không có căn nào vượt qua đầy đủ "
                "tiêu chí khoảng cách/thời gian di chuyển đã yêu cầu."
            )
        if criteria.get("transaction_type") == "SALE" and criteria.get("max_price") and criteria["max_price"] < 100_000_000:
            low_p = criteria["max_price"]
            return {
                "selected_properties": [],
                "search_results": [],
                "response": (
                    f"Mức giá **{_price_text(low_p)}** thường là ngân sách dành cho việc **thuê căn hộ / phòng trọ hằng tháng**, "
                    f"vì trên thị trường hiện tại không có bất động sản mở bán với mức giá này.\n\n"
                    f"💡 **Bạn đang muốn:**\n"
                    f"- **Tìm thuê căn hộ** với ngân sách khoảng {_price_text(low_p)}/tháng?\n"
                    f"- Hay bạn dự định **tìm mua căn hộ** khoảng **{_price_text(low_p * 1000)}**?"
                ),
                "response_kind": "SEARCH_NO_RESULTS",
                "phase": "SEARCH_NO_RESULTS",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": [
                    f"Tìm thuê căn hộ {_price_text(low_p)}/tháng",
                    f"Tìm mua căn hộ {_price_text(low_p * 1000)}",
                    "Điều chỉnh ngân sách",
                ],
            }
        if criteria.get("target_price") or (criteria.get("min_price") and criteria.get("max_price")):
            target_p = criteria.get("target_price") or ((criteria["min_price"] + criteria["max_price"]) / 2)
            location_name = criteria.get("district") or criteria.get("province") or "khu vực này"

            # Query location without price filter to analyze available segments
            loc_criteria = {k: v for k, v in criteria.items() if k not in ("min_price", "max_price", "target_price")}
            all_loc_props = await query_properties_from_db(loc_criteria, limit=20)

            lower_props = [p for p in all_loc_props if (p.get("list_price") or 0) < target_p]
            higher_props = [p for p in all_loc_props if (p.get("list_price") or 0) > target_p]

            max_lower = max((p.get("list_price") or 0) for p in lower_props) if lower_props else None
            min_higher = min((p.get("list_price") or 0) for p in higher_props) if higher_props else None

            min_window_str = _price_text(criteria.get("min_price", round(target_p * 0.8)))
            max_window_str = _price_text(criteria.get("max_price", round(target_p * 1.2)))

            lines = [
                f"Hiện tại trong kho dữ liệu tại **{location_name}**, Nera chưa có bất động sản nào trong tầm giá **{min_window_str} – {max_window_str}** (quanh mức **{_price_text(target_p)}** bạn yêu cầu).\n",
            ]

            if max_lower or min_higher:
                lines.append(f"📊 **Các phân khúc hiện có tại {location_name}:**")
                if max_lower:
                    lines.append(f"- Phân khúc giá thấp hơn: **dưới {_price_text(max_lower)}**")
                if min_higher:
                    lines.append(f"- Phân khúc cao cấp hơn: **từ {_price_text(min_higher)} trở lên**")
                lines.append("")

            lines.append("💡 **Gợi ý từ Nera:**")
            lines.append(f"- Mở rộng tìm kiếm tầm giá {_price_text(target_p)} sang các quận lân cận")
            if max_lower:
                lines.append(f"- Tham khảo các căn dưới {_price_text(max_lower)} tại {location_name}")
            if min_higher:
                lines.append(f"- Tham khảo các căn từ {_price_text(min_higher)} tại {location_name}")

            suggested = [f"Tìm nhà {_price_text(target_p)} ở quận lân cận"]
            if max_lower:
                suggested.append(f"Xem căn dưới {_price_text(max_lower)} ở {location_name}")
            if min_higher:
                suggested.append(f"Xem căn từ {_price_text(min_higher)} ở {location_name}")
            if len(suggested) < 3:
                suggested.append("Tư vấn khu vực phù hợp")

            return {
                "selected_properties": [],
                "search_results": [],
                "response": "\n".join(lines),
                "response_kind": "SEARCH_NO_RESULTS",
                "phase": "SEARCH_NO_RESULTS",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": suggested[:3],
            }

        if criteria.get("transaction_type") == "RENT":
            rental_total = await count_rental_listings()
            if rental_total == 0:
                # Saying "chưa khớp tiêu chí" would imply rentals exist and the
                # filters were too tight. They do not exist at all, and the
                # customer deserves to hear that before they keep rewording.
                response = (
                    "Nera nói thật với bạn: kho hiện tại **chỉ có tin bán, chưa có tin cho thuê nào**. "
                    "Nera sẽ không đưa tin bán vào kết quả thuê để bạn khỏi mất công xem nhầm.\n\n"
                    "Nếu bạn đang cân nhắc mua, Nera tìm giúp ngay. Còn nhu cầu thuê thì bạn quay lại "
                    "sau nhé, nhóm đang bổ sung nguồn tin thuê."
                )
                actions = ["Tìm nhà để mua", "Xem tất cả căn đang có"]
            else:
                response = (
                    "Kho dữ liệu hiện tại chưa có tin **cho thuê** khớp tiêu chí của bạn. "
                    "Nera sẽ không trộn các tin bán vào kết quả thuê. Bạn có thể đổi khu vực, "
                    "ngân sách thuê hoặc chuyển sang nhu cầu mua."
                )
                actions = ["Đổi khu vực thuê", "Điều chỉnh ngân sách", "Tìm nhà để mua"]
            return {
                "selected_properties": [],
                "search_results": [],
                "response": response,
                "response_kind": "SEARCH_NO_RESULTS",
                "phase": "SEARCH_NO_RESULTS",
                "current_agent": AgentType.RESPOND,
                "suggested_actions": actions,
            }
        return {
            "selected_properties": [],
            "search_results": [],
            "response": f"{(geo_note + chr(10) + chr(10)) if geo_note else ''}Rất tiếc mình chưa tìm thấy bất động sản nào khớp hoàn toàn với tiêu chí **{summary or 'hiện tại'}**.\n\n💡 **Gợi ý điều chỉnh:**\n- Thử nới rộng ngân sách hoặc mở rộng sang các quận lân cận\n- Giảm bớt yêu cầu số phòng ngủ hoặc diện tích tối thiểu\n\nMình vẫn đang giữ các tiêu chí khác của bạn. Bạn muốn điều chỉnh phần nào?",
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

    search_response_text = await format_intelligent_search_results(
        properties,
        criteria,
        soft_prefs,
        query,
        affordability_note=state.get("affordability_note"),
        is_resume=False,
    )

    return {
        "selected_properties": properties,
        "search_results": properties,
        "current_property_id": None,
        "selected_property_index": None,
        "response": (
            f"⚠️ {geo_note}\n\n" if geo_note else ""
        ) + search_response_text,
        "response_kind": "SEARCH_RESULTS",
        "phase": "SEARCH_RESULTS",
        "current_agent": AgentType.RESPOND,
        "suggested_actions": suggested_actions,
    }
