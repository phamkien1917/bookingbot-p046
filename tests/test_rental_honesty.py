"""When the store holds no rentals, Nera must say so instead of stalling.

"Chưa khớp tiêu chí" implies rentals exist and the filters were too tight. If
there are none at all, that answer sends the customer round in circles
rewording a query that can never return anything.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.agents.nodes.inventory_agent import inventory_agent
from src.agents.state import Intent, create_initial_agent_state


def _rental_search_state(query: str = "tìm phòng trọ ở Cầu Giấy"):
    state = create_initial_agent_state(session_id="rent-test", query=query)
    state["intent"] = Intent.SEARCH_PROPERTY
    state["search_criteria"] = {"transaction_type": "RENT", "district": "Cầu Giấy"}
    return state


async def _run(rental_total: int) -> dict:
    with (
        patch(
            "src.agents.nodes.inventory_agent.query_properties_from_db",
            AsyncMock(return_value=[]),
        ),
        patch(
            "src.agents.nodes.inventory_agent.count_rental_listings",
            AsyncMock(return_value=rental_total),
        ),
    ):
        return await inventory_agent(_rental_search_state())


@pytest.mark.asyncio
async def test_an_empty_rental_store_is_admitted_outright() -> None:
    result = await _run(rental_total=0)

    assert "chưa có tin cho thuê nào" in result["response"]
    assert result["selected_properties"] == []
    # Rewording the search cannot help, so it must not be offered as a way out.
    assert "Điều chỉnh ngân sách" not in result["suggested_actions"]


@pytest.mark.asyncio
async def test_rentals_that_exist_but_do_not_match_invite_a_rewording() -> None:
    result = await _run(rental_total=12)

    assert "chưa có tin cho thuê nào" not in result["response"]
    assert "Điều chỉnh ngân sách" in result["suggested_actions"]


@pytest.mark.asyncio
async def test_sale_listings_are_never_offered_as_rentals() -> None:
    for total in (0, 12):
        result = await _run(rental_total=total)
        assert result["search_results"] == []
