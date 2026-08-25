"""Main LangGraph workflow for BookingBot AI Multi-Agent System."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from langgraph.graph import END, StateGraph

from src.agents.nodes import (
    assignment_agent,
    booking_agent,
    hitl_agent,
    inventory_agent,
    respond_node,
    route_from_supervisor,
    supervisor_node,
)
from src.agents.state import AgentState

logger = logging.getLogger(__name__)


def build_agent_graph() -> StateGraph:
    """Build the compiled multi-agent state graph."""
    graph = StateGraph(AgentState)

    # Add all agent nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("inventory", inventory_agent)
    graph.add_node("booking", booking_agent)
    graph.add_node("assignment", assignment_agent)
    graph.add_node("hitl", hitl_agent)
    graph.add_node("respond", respond_node)

    # Set entry point
    graph.set_entry_point("supervisor")

    # Supervisor conditional routing
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "inventory": "inventory",
            "booking": "booking",
            "assignment": "assignment",
            "hitl": "hitl",
            "respond": "respond",
            "__end__": END,
        },
    )

    # All worker nodes transition to respond node to finalize the output
    graph.add_edge("inventory", "respond")
    graph.add_edge("booking", "respond")
    graph.add_edge("assignment", "respond")
    graph.add_edge("hitl", "respond")
    graph.add_edge("respond", END)

    return graph.compile()


_compiled_agent = None


def get_agent_graph():
    """Get singleton compiled agent graph."""
    global _compiled_agent
    if _compiled_agent is None:
        _compiled_agent = build_agent_graph()
    return _compiled_agent


async def run_agent(
    state: AgentState,
    on_stage: Callable[[str], None] | None = None,
) -> AgentState:
    """Execute the multi-agent graph with error boundary and recovery.

    When `on_stage` is given the graph is streamed node by node and the callback
    receives each node name as it finishes, so a caller can report real progress
    instead of guessing at it. The result is identical either way: AgentState is a
    plain TypedDict with no reducers, so merging the per-node updates in order
    produces what ainvoke would have returned.
    """
    graph = get_agent_graph()
    try:
        if on_stage is None:
            return await graph.ainvoke(state)

        merged: dict[str, Any] = dict(state)
        async for chunk in graph.astream(state, stream_mode="updates"):
            for node_name, updates in chunk.items():
                if isinstance(updates, dict):
                    merged.update(updates)
                on_stage(node_name)
        return merged  # type: ignore[return-value]
    except Exception as exc:
        logger.exception("Error executing LangGraph agent: %s", exc)
        fallback_state = dict(state)
        fallback_state["response"] = (
            "Chào bạn, mình là Nera. Mình vừa gặp chút gián đoạn kết nối hệ thống. "
            "Bạn có thể nhắn lại yêu cầu (ví dụ: tìm nhà ở đâu, khoảng giá bao nhiêu) để mình hỗ trợ ngay nhé!"
        )
        fallback_state["ai_mode"] = "fallback"
        fallback_state["error"] = str(exc)
        return fallback_state
