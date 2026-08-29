"""The graph must report where a turn's time actually goes.

ai_latency_ms only ever counted the supervisor, so the inventory and respond
LLM calls were invisible. These cover the wrapper that fixes that.
"""

import asyncio

import pytest

from src.agents.graph import _timed


@pytest.mark.asyncio
async def test_timed_records_the_node_under_its_own_name():
    async def node(state):
        await asyncio.sleep(0.01)
        return {"response": "ok"}

    result = await _timed("respond", node)({})

    assert result["response"] == "ok"
    assert result["stage_timings"]["respond"] >= 10


@pytest.mark.asyncio
async def test_timed_keeps_timings_recorded_by_earlier_nodes():
    async def node(state):
        return {}

    result = await _timed("respond", node)({"stage_timings": {"supervisor": 42}})

    assert result["stage_timings"]["supervisor"] == 42
    assert "respond" in result["stage_timings"]


@pytest.mark.asyncio
async def test_timed_sums_repeat_visits_to_the_same_node():
    """A node reached twice in one turn must add up, not overwrite."""

    async def node(state):
        return {}

    wrapped = _timed("booking", node)
    first = await wrapped({})
    second = await wrapped(first)

    assert second["stage_timings"]["booking"] >= first["stage_timings"]["booking"]


@pytest.mark.asyncio
async def test_timed_passes_through_a_non_dict_result():
    async def node(state):
        return None

    assert await _timed("hitl", node)({}) is None
