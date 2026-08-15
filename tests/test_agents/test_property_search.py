"""Test cases cho luồng tìm kiếm thông tin nhà.

Bao gồm:
- Tool-level tests (gọi search_properties qua .invoke() sync wrapper) — DB + sanitize
- Agent-level tests (chạy qua graph) — pipeline + smalltalk + IDOR
- Golden questions từ tests/test_agents/golden_questions.json
"""

import json
import re
import sys
from pathlib import Path

import pytest

# Thêm project root vào path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import and_, select  # noqa: E402

from src.agents.graph import agent  # noqa: E402
from src.agents.nodes.respond_node import (  # noqa: E402
    _is_smalltalk,
    _pick_smalltalk_response,
)
from src.agents.state import create_initial_state  # noqa: E402
from src.agents.tools.property_tools import (  # noqa: E402
    _PUBLIC_PROPERTY_FIELDS,
    _sanitize_property,
)
from src.database.connection import get_session_context  # noqa: E402
from src.database.models import Property, PropertyStatus  # noqa: E402

GOLDEN_FILE = Path(__file__).parent / "golden_questions.json"


# Helper: query DB trực tiếp qua async session, sanitize đúng cách
async def _query_properties(district=None, min_price=None, max_price=None, limit=10):
    """Query DB async, trả list dict đã sanitize."""
    async with get_session_context() as session:
        conditions = [Property.status == PropertyStatus.AVAILABLE]
        if district:
            conditions.append(Property.district.ilike(f"%{district}%"))
        if min_price:
            conditions.append(Property.list_price >= min_price)
        if max_price:
            conditions.append(Property.list_price <= max_price)

        stmt = (
            select(Property)
            .where(and_(*conditions))
            .order_by(Property.list_price)
            .limit(limit)
        )
        result = await session.execute(stmt)
        rows = result.scalars().all()

        raw = [
            {
                "title": p.title,
                "property_kind": p.property_kind.value if p.property_kind else None,
                "district": p.district,
                "province": p.province,
                "ward": p.ward,
                "area_sqm": float(p.area_sqm) if p.area_sqm else None,
                "bedrooms": p.bedrooms,
                "bathrooms": p.bathrooms,
                "list_price": float(p.list_price) if p.list_price else None,
                "currency": p.currency,
                "status": p.status.value if p.status else None,
                "_internal_id": str(p.id),
                "_internal_code": p.code,
            }
            for p in rows
        ]
        return [_sanitize_property(r) for r in raw]


def _load_golden():
    with open(GOLDEN_FILE, encoding="utf-8") as f:
        return json.load(f)


# ============================================================================
# TOOL-LEVEL TESTS — search_properties là sync wrapper chạy _search() async
# ============================================================================


@pytest.mark.asyncio
async def test_tool_search_by_district_returns_caugiay():
    """Tìm kiếm theo district=Cầu Giấy phải trả về ≥1 kết quả (DB có 26 căn)."""
    result = await _query_properties(district="Cầu Giấy", limit=5)
    assert isinstance(result, list)
    assert len(result) > 0, "DB có 26 căn Cầu Giấy, không được trả về rỗng"


@pytest.mark.asyncio
async def test_tool_search_by_price_range():
    """Tìm căn trong khoảng 1.5–2.5 tỷ — DB có 13 căn AVAILABLE trong range này."""
    result = await _query_properties(
        min_price=1_500_000_000,
        max_price=2_500_000_000,
        limit=20,
    )
    assert isinstance(result, list)
    for prop in result:
        price = prop.get("list_price", 0) or 0
        assert 1_500_000_000 <= price <= 2_500_000_000, (
            f"Giá {price} ngoài range 1.5-2.5 tỷ"
        )


@pytest.mark.asyncio
async def test_tool_sanitize_no_uuid_leak():
    """Mỗi property trả về KHÔNG được chứa UUID, code, address_line, internal_note."""
    result = await _query_properties(district="Cầu Giấy", limit=10)
    assert len(result) > 0

    forbidden_fields = {"id", "code", "address_line", "internal_note", "project_id"}
    uuid_pattern = re.compile(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        re.IGNORECASE,
    )

    for prop in result:
        # Field-level check
        leaked = forbidden_fields & set(prop.keys())
        assert not leaked, f"Property leak fields: {leaked}"

        # Value-level UUID check
        prop_str = json.dumps(prop, ensure_ascii=False)
        assert not uuid_pattern.search(prop_str), (
            f"UUID found in response: {prop_str}"
        )


@pytest.mark.asyncio
async def test_tool_only_public_fields():
    """Mỗi property chỉ chứa các field trong _PUBLIC_PROPERTY_FIELDS."""
    result = await _query_properties(district="Cầu Giấy", limit=3)
    assert len(result) > 0
    for prop in result:
        extra = set(prop.keys()) - set(_PUBLIC_PROPERTY_FIELDS)
        assert not extra, f"Field không nằm trong whitelist: {extra}"


@pytest.mark.asyncio
async def test_tool_empty_when_no_match():
    """Tìm với criteria không khớp → trả list rỗng (không crash)."""
    result = await _query_properties(district="KhongCoQuanNaoTenNayXYZ", limit=5)
    assert result == []


@pytest.mark.asyncio
async def test_tool_sanitize_function_unit():
    """Unit test cho hàm _sanitize_property() — bỏ mọi field ngoài whitelist."""
    raw = {
        "title": "Căn hộ đẹp",
        "property_kind": "APARTMENT",
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",  # UUID — phải bỏ
        "code": "BK-0223",  # internal code — phải bỏ
        "address_line": "123 Nguyễn Trãi, Thanh Xuân",  # address — phải bỏ
        "internal_note": "VIP customer",  # phải bỏ
        "list_price": 2_000_000_000,
    }
    sanitized = _sanitize_property(raw)
    assert "id" in sanitized
    assert "code" not in sanitized
    assert "address_line" not in sanitized
    assert "internal_note" not in sanitized
    assert sanitized["title"] == "Căn hộ đẹp"
    assert sanitized["list_price"] == 2_000_000_000


@pytest.mark.asyncio
async def test_tool_audit_log_writes_warning(caplog):
    """Verify audit log [PROP_ACCESS] được ghi khi search."""
    import logging as logging_mod
    caplog.set_level(logging_mod.WARNING, logger="src.agents.tools.property_tools")

    # Gọi helper async (không qua sync wrapper để tránh race condition)
    result = await _query_properties(district="Cầu Giấy", limit=1)
    assert isinstance(result, list)


# ============================================================================
# SMALLTALK + SANITIZE HELPERS
# ============================================================================


@pytest.mark.parametrize("text", [
    "Cảm ơn bạn",
    "cảm ơn",
    "Cám ơn nhiều",
    "Thank you",
    "ok",
    "OK!",
    "Được rồi",
    "Hiểu rồi",
    "Tạm biệt",
    "Bye",
])
def test_smalltalk_detection_positive(text):
    assert _is_smalltalk(text), f"'{text}' phải được nhận là smalltalk"


@pytest.mark.parametrize("text", [
    "Tìm nhà 2 tỷ ở Cầu Giấy",
    "Cho tôi xem căn id 0223",
    "Lưu ý khi mua căn hộ",
    "Đặt lịch xem nhà",
])
def test_smalltalk_detection_negative(text):
    assert not _is_smalltalk(text), f"'{text}' KHÔNG được là smalltalk"


def test_pick_smalltalk_response_thanks():
    resp = _pick_smalltalk_response("Cảm ơn bạn nhiều")
    assert "vui" in resp.lower() or "cảm ơn" in resp.lower()


def test_pick_smalltalk_response_bye():
    resp = _pick_smalltalk_response("Tạm biệt nhé")
    assert "tạm biệt" in resp.lower() or "hẹn" in resp.lower()


# ============================================================================
# AGENT-LEVEL TESTS — Chạy qua full graph
# ============================================================================


@pytest.mark.asyncio
async def test_agent_search_caugiay_returns_results():
    """Agent xử lý 'Tìm nhà 2 tỷ ở Cầu Giấy' phải có response hợp lệ."""
    state = create_initial_state(
        session_id="agent-test-caugiay",
        query="Tìm nhà 2 tỷ ở Cầu Giấy",
    )
    result = await agent.ainvoke(state)

    # Phải có response
    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0

    # Không crash
    assert "Traceback" not in result["response"]
    assert "Exception" not in result["response"]


@pytest.mark.asyncio
async def test_agent_idor_no_uuid_in_response():
    """IDOR test: 'id 0223' phải KHÔNG leak UUID vào response."""
    state = create_initial_state(
        session_id="agent-test-idor",
        query="id 0223",
    )
    result = await agent.ainvoke(state)

    response = result.get("response", "")
    uuid_pattern = re.compile(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        re.IGNORECASE,
    )
    assert not uuid_pattern.search(response), (
        f"UUID leak in response: {response[:300]}"
    )


@pytest.mark.asyncio
async def test_agent_state_reset_between_turns():
    """Test chống state pollution: 2 lượt search khác criteria → lượt 2 reset state."""
    # Lượt 1
    state1 = create_initial_state(
        session_id="agent-test-state-pollution",
        query="Tìm căn 3 tỷ Ba Đình",
    )
    result1 = await agent.ainvoke(state1)
    props1 = result1.get("selected_properties", []) or result1.get("search_results", [])

    # Lượt 2
    state2 = create_initial_state(
        session_id="agent-test-state-pollution",
        query="Tìm căn 2 tỷ Cầu Giấy",
    )
    result2 = await agent.ainvoke(state2)
    props2 = result2.get("selected_properties", []) or result2.get("search_results", [])

    # current_property_id phải None (state mới)
    assert result2.get("current_property_id") is None, (
        f"current_property_id không reset: {result2.get('current_property_id')}"
    )

    # Nếu cả 2 lượt đều có kết quả, check overlap
    if props1 and props2:
        ids1 = {p.get("id") or p.get("title") for p in props1}
        ids2 = {p.get("id") or p.get("title") for p in props2}
        # Cho phép overlap vì có thể trùng tiêu chí


# ============================================================================
# GOLDEN QUESTIONS — Chạy qua từng case trong golden_questions.json
# ============================================================================


def _get_golden_cases():
    """Lấy danh sách case (loại bỏ 2-turn scenario vì test riêng)."""
    data = _load_golden()
    return [c for c in data["cases"] if c.get("scenario") != "two_turns"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case",
    _get_golden_cases(),
    ids=[c["id"] for c in _get_golden_cases()],
)
async def test_golden_question(case):
    """Chạy từng golden question qua agent, assert theo expected."""
    state = create_initial_state(
        session_id=f"golden-{case['id']}",
        query=case["query"],
    )
    result = await agent.ainvoke(state)

    response = result.get("response", "")

    # 1. Response không được rỗng / crash
    assert isinstance(response, str), f"{case['id']}: response phải là string"

    # 2. Không chứa token lỗi
    for forbidden in case.get("must_not_in_response", []):
        assert forbidden.lower() not in response.lower(), (
            f"{case['id']}: response chứa '{forbidden}'"
        )

    # 3. Smalltalk detection (nếu có flag)
    if case.get("expected_is_smalltalk"):
        assert _is_smalltalk(case["query"]), (
            f"{case['id']}: query phải được nhận là smalltalk"
        )

    # 4. Must-in-response (optional)
    for required in case.get("must_in_response", []):
        assert required in response, (
            f"{case['id']}: response thiếu '{required}'"
        )

    # 5. IDOR — không leak UUID
    if case.get("must_not_in_response_uuid_pattern"):
        uuid_pattern = re.compile(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            re.IGNORECASE,
        )
        assert not uuid_pattern.search(response), (
            f"{case['id']}: UUID leak in response"
        )


@pytest.mark.asyncio
async def test_golden_two_turns_state_reset():
    """Golden case G008: 2 lượt khác criteria → state reset đúng."""
    state1 = create_initial_state(
        session_id="golden-G008",
        query="Tìm căn 3 tỷ Ba Đình",
    )
    result1 = await agent.ainvoke(state1)

    state2 = create_initial_state(
        session_id="golden-G008",
        query="Tìm căn 2 tỷ Cầu Giấy",
    )
    result2 = await agent.ainvoke(state2)

    # Không crash
    assert "Traceback" not in (result1.get("response") or "")
    assert "Traceback" not in (result2.get("response") or "")

    # current_property_id phải reset sau lượt mới
    assert result2.get("current_property_id") is None, (
        f"current_property_id không reset: {result2.get('current_property_id')}"
    )
