"""Streaming must not change what a turn produces, only how it is observed.

run_agent merges per-node updates when a progress callback is supplied. These
tests pin the assumption that makes it safe: AgentState carries no reducers, so
merging updates in order equals what ainvoke returns.
"""

from typing import Any, TypedDict

import pytest
from langgraph.graph import END, StateGraph


class _State(TypedDict, total=False):
    trail: str
    value: int
    untouched: str


def _first(state: _State) -> dict[str, Any]:
    return {"trail": (state.get("trail") or "") + "a", "value": 1}


def _second(state: _State) -> dict[str, Any]:
    return {"trail": (state.get("trail") or "") + "b", "value": state.get("value", 0) + 10}


def _build() -> Any:
    graph = StateGraph(_State)
    graph.add_node("first", _first)
    graph.add_node("second", _second)
    graph.set_entry_point("first")
    graph.add_edge("first", "second")
    graph.add_edge("second", END)
    return graph.compile()


@pytest.mark.asyncio
async def test_merged_updates_equal_ainvoke() -> None:
    graph = _build()
    start: _State = {"untouched": "keep me"}

    invoked = await graph.ainvoke(dict(start))

    merged: dict[str, Any] = dict(start)
    async for chunk in graph.astream(dict(start), stream_mode="updates"):
        for _node, updates in chunk.items():
            if isinstance(updates, dict):
                merged.update(updates)

    assert merged == invoked
    assert merged["trail"] == "ab"
    assert merged["value"] == 11
    assert merged["untouched"] == "keep me"


@pytest.mark.asyncio
async def test_every_node_is_reported_once_and_in_order() -> None:
    graph = _build()
    seen: list[str] = []

    async for chunk in graph.astream({"untouched": "x"}, stream_mode="updates"):
        seen.extend(chunk.keys())

    assert seen == ["first", "second"]


@pytest.mark.asyncio
async def test_agent_state_has_no_reducers() -> None:
    """The merge above is only valid while AgentState stays a plain TypedDict.

    If someone adds an Annotated field with a reducer, merging updates would
    silently diverge from ainvoke and this test should fail loudly first.
    """
    from src.agents.state import AgentState

    hints = getattr(AgentState, "__annotations__", {})
    assert hints, "AgentState should declare fields"
    for name, hint in hints.items():
        assert "Annotated" not in str(hint), (
            f"{name} uses Annotated; run_agent's update merge assumes no reducers"
        )
