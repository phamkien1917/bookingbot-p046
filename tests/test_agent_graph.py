"""The graph end to end, with no model and no database behind it.

This is the integration layer of the pyramid: not "did the supervisor classify
well" — that is the golden set's job — but "does a turn entered at the top come
out the bottom with a reply, having passed through the nodes it was supposed
to". A graph wired wrong fails here even when every node is right on its own.
"""

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from src.agents.graph import build_agent_graph, get_agent_graph
from src.agents.state import AgentType, create_initial_agent_state


@pytest.fixture(autouse=True)
def offline_llm():
    """No test in this file may reach a provider.

    respond_node calls get_llm() unconditionally. Left alone, each of these
    tests spent several seconds on a live request that failed into the
    rule-based fallback — a real bill and a real flake, for a result the test
    never looked at.
    """
    llm = AsyncMock()
    llm.ainvoke = AsyncMock(return_value=SimpleNamespace(content="Chào bạn."))
    with patch("src.agents.nodes.respond_node.get_llm", return_value=llm):
        yield llm


def initial(query: str, session_id: str = "test-graph") -> dict[str, Any]:
    return dict(create_initial_agent_state(session_id=session_id, query=query))


def stub_supervisor(agent: str = AgentType.RESPOND, **extra: Any):
    """Replace the supervisor so the turn takes a chosen branch, model-free."""

    async def _node(state: dict[str, Any]) -> dict[str, Any]:
        return {**state, "current_agent": agent, "intent": "GREETING", **extra}

    return _node


@pytest.mark.asyncio
async def test_a_turn_entered_at_the_top_comes_out_with_a_reply():
    assert get_agent_graph() is not None, "the cached graph builds"

    with patch("src.agents.graph.supervisor_node", stub_supervisor()):
        result = await build_agent_graph().ainvoke(initial("Xin chào!"))

    assert isinstance(result.get("response"), str)
    assert result["response"].strip(), "a turn that reaches respond must say something"


@pytest.mark.asyncio
async def test_an_empty_query_still_answers_rather_than_crashing():
    """The endpoint validates empties away, but the graph must not rely on that."""
    with patch("src.agents.graph.supervisor_node", stub_supervisor()):
        result = await build_agent_graph().ainvoke(initial(""))

    assert result is not None
    assert "response" in result


@pytest.mark.asyncio
async def test_a_worker_that_wants_a_human_is_routed_through_hitl():
    """The branch that matters most: booking must not answer past the gate."""
    seen: list[str] = []

    async def booking(state: dict[str, Any]) -> dict[str, Any]:
        seen.append("booking")
        return {**state, "awaiting_human": True, "response": "Đang chờ sale duyệt."}

    async def hitl(state: dict[str, Any]) -> dict[str, Any]:
        seen.append("hitl")
        return state

    with (
        patch("src.agents.graph.supervisor_node", stub_supervisor(AgentType.BOOKING)),
        patch("src.agents.graph.booking_agent", booking),
        patch("src.agents.graph.hitl_agent", hitl),
    ):
        await build_agent_graph().ainvoke(initial("Đặt lịch xem căn 1"))

    assert seen == ["booking", "hitl"], "a booking awaiting approval skipped the HITL node"


@pytest.mark.asyncio
async def test_a_finished_worker_goes_straight_to_respond():
    seen: list[str] = []

    async def booking(state: dict[str, Any]) -> dict[str, Any]:
        seen.append("booking")
        return {**state, "awaiting_human": False, "response": "Đã ghi nhận."}

    async def hitl(state: dict[str, Any]) -> dict[str, Any]:
        seen.append("hitl")
        return state

    with (
        patch("src.agents.graph.supervisor_node", stub_supervisor(AgentType.BOOKING)),
        patch("src.agents.graph.booking_agent", booking),
        patch("src.agents.graph.hitl_agent", hitl),
    ):
        await build_agent_graph().ainvoke(initial("Đặt lịch xem căn 1"))

    assert seen == ["booking"], "a finished booking was sent to a human anyway"


@pytest.mark.asyncio
async def test_every_node_reports_how_long_it_took():
    """stage_timings is what the latency reports in eval/results are built from.

    A node added without the _timed wrapper would silently vanish from every
    latency measurement the team publishes.
    """
    async def inventory(state: dict[str, Any]) -> dict[str, Any]:
        return state

    with (
        patch("src.agents.graph.supervisor_node", stub_supervisor(AgentType.INVENTORY)),
        patch("src.agents.graph.inventory_agent", inventory),
    ):
        result = await build_agent_graph().ainvoke(initial("Tìm nhà Cầu Giấy"))

    timings = result.get("stage_timings") or {}
    assert timings, "no node recorded a duration"
    assert {"supervisor", "inventory", "respond"} <= set(timings)
    assert all(isinstance(ms, (int, float)) and ms >= 0 for ms in timings.values())
