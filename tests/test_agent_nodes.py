"""Individual nodes, one at a time, with the model replaced.

The bottom of the pyramid. The graph tests prove the wiring; the golden set
proves the wording. These prove that a node handed a given understanding turns
it into the state the next node expects — the part that breaks quietly, because
a wrong `current_agent` still produces a fluent answer from the wrong worker.

Every test here stubs `ainvoke_structured`, so the supervisor's own routing and
post-processing runs for real while the model does not.
"""

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from src.agents.nodes.supervisor import (
    SupervisorUnderstanding,
    _extract_booking_code,
    _is_generic_geo_category_landmark,
    supervisor_node,
)
from src.agents.state import AgentType, Intent, create_initial_agent_state


def state_for(query: str, **extra: Any) -> dict[str, Any]:
    base = dict(create_initial_agent_state(session_id="test-node", query=query))
    base.update(extra)
    return base


def stub_llm(understanding: SupervisorUnderstanding):
    """An LLM that returns one fixed understanding, and no tokens."""
    llm = AsyncMock()
    llm.ainvoke_structured = AsyncMock(return_value=understanding)
    llm.ainvoke = AsyncMock(return_value=SimpleNamespace(content=""))
    return llm


async def run_supervisor(query: str, understanding: SupervisorUnderstanding, **extra: Any):
    with patch("src.agents.nodes.supervisor.get_llm", return_value=stub_llm(understanding)):
        return await supervisor_node(state_for(query, **extra))


# ── Pure helpers ─────────────────────────────────────────────────────────────


class TestExtractBookingCode:
    @pytest.mark.parametrize(
        "message,expected",
        [
            ("Cho mình hỏi mã BK2024ABC", "BK2024ABC"),
            ("mã bk2024abc của mình", "BK2024ABC"),
            ("Đơn TR-9F8E7D thế nào rồi", "TR-9F8E7D"),
            ("Tìm nhà ở Cầu Giấy", None),
            ("", None),
        ],
    )
    def test_only_a_real_code_is_pulled_out(self, message, expected):
        assert _extract_booking_code(message) == expected


class TestGenericGeoLandmark:
    """A category is not a destination; Places resolves those, not the router."""

    @pytest.mark.parametrize(
        "value", ["bệnh viện", "trường học", "siêu thị", "công viên gần đây"]
    )
    def test_a_bare_category_is_rejected(self, value):
        assert _is_generic_geo_category_landmark(value) is True

    @pytest.mark.parametrize(
        "value", ["Đại học Quốc gia Hà Nội", "Bệnh viện Bạch Mai", "Vincom Bà Triệu"]
    )
    def test_a_named_place_is_kept(self, value):
        assert _is_generic_geo_category_landmark(value) is False

    def test_nothing_is_not_a_landmark(self):
        assert _is_generic_geo_category_landmark(None) is False
        assert _is_generic_geo_category_landmark("") is False


# ── The supervisor node itself ───────────────────────────────────────────────


class TestSupervisorRouting:
    """Which worker each intent hands the turn to."""

    @pytest.mark.asyncio
    async def test_a_search_goes_to_inventory(self):
        result = await run_supervisor(
            "Tìm căn 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ",
            SupervisorUnderstanding(intent=Intent.SEARCH_PROPERTY, confidence=0.95),
        )

        assert result["current_agent"] == AgentType.INVENTORY
        assert result["intent"] == Intent.SEARCH_PROPERTY

    @pytest.mark.asyncio
    async def test_a_booking_goes_to_booking(self):
        result = await run_supervisor(
            "Đặt lịch xem căn số 1 vào 9h sáng mai",
            SupervisorUnderstanding(intent=Intent.BOOK_APPOINTMENT, confidence=0.9),
        )

        assert result["current_agent"] == AgentType.BOOKING

    @pytest.mark.asyncio
    async def test_a_greeting_answers_without_a_worker(self):
        """Small talk must not spend a database query or a geo call."""
        result = await run_supervisor(
            "Xin chào", SupervisorUnderstanding(intent=Intent.GREETING, confidence=1.0)
        )

        assert result["current_agent"] == AgentType.RESPOND

    @pytest.mark.asyncio
    async def test_an_out_of_scope_question_does_not_reach_inventory(self):
        """The guardrail: an unrelated question must not become a search."""
        result = await run_supervisor(
            "Tháp Eiffel cao bao nhiêu mét?",
            SupervisorUnderstanding(intent=Intent.OUT_OF_SCOPE, confidence=1.0),
        )

        assert result["current_agent"] != AgentType.INVENTORY


class TestSupervisorCriteria:
    """What the supervisor writes into search_criteria for inventory to use."""

    @pytest.mark.asyncio
    async def test_stated_constraints_survive_into_the_criteria(self):
        result = await run_supervisor(
            "Tìm căn 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ",
            SupervisorUnderstanding(intent=Intent.SEARCH_PROPERTY, is_new_search=True),
        )

        criteria = result.get("search_criteria") or {}
        assert criteria.get("max_price") == 5_000_000_000
        assert criteria.get("exact_bedrooms") == 2 or criteria.get("min_bedrooms") == 2

    @pytest.mark.asyncio
    async def test_an_income_is_not_read_as_a_price(self):
        """The bug this backstop exists for: 40 triệu/tháng became a 40 tỷ budget."""
        result = await run_supervisor(
            "Thu nhập mình 40 triệu một tháng thì mua được căn nào",
            SupervisorUnderstanding(intent=Intent.CONSULTATION_QA),
        )

        criteria = result.get("search_criteria") or {}
        assert criteria.get("max_price") != 40_000_000_000
        assert result.get("monthly_income_vnd") == 40_000_000


class TestSupervisorResilience:
    @pytest.mark.asyncio
    async def test_a_provider_failure_still_produces_a_routable_state(self):
        """A dead provider degrades the turn; it must not drop it."""
        llm = AsyncMock()
        llm.ainvoke_structured = AsyncMock(side_effect=RuntimeError("provider down"))

        with patch("src.agents.nodes.supervisor.get_llm", return_value=llm):
            result = await supervisor_node(state_for("Tìm nhà ở Cầu Giấy"))

        assert result.get("current_agent"), "a failed turn was left with nowhere to go"
        assert result["current_agent"] in {
            AgentType.INVENTORY,
            AgentType.BOOKING,
            AgentType.ASSIGNMENT,
            AgentType.HITL,
            AgentType.RESPOND,
        }

    @pytest.mark.asyncio
    async def test_an_empty_query_is_survivable(self):
        result = await run_supervisor(
            "", SupervisorUnderstanding(intent=Intent.FALLBACK, confidence=0.1)
        )

        assert result.get("current_agent")
