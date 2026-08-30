"""Main LangGraph workflow for BookingBot AI Multi-Agent System."""

from __future__ import annotations

import logging
import os
import time
from collections.abc import Callable
from functools import lru_cache
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


def _route_after_worker(state: AgentState) -> str:
    """Escalate worker failures into the durable HITL queue.

    The case id is no longer skipped over: it now survives between turns, and
    hitl_agent is the node that decides what to do with it — report the case as
    pending, deliver a resolved decision, or open a new one. Routing past it on a
    known id would strand the customer on a case they never hear back about.
    """
    return "hitl" if state.get("awaiting_human") else "respond"


def _timed(name: str, node: Callable) -> Callable:
    """Record how long a node took under state["stage_timings"].

    Only the supervisor used to time itself, so ai_latency_ms hid the cost of the
    inventory and respond LLM calls. Wrapping here covers every node at once,
    including any added later.
    """

    async def wrapper(state: AgentState) -> dict:
        started = time.perf_counter()
        result = await node(state)
        elapsed = round((time.perf_counter() - started) * 1000)
        if not isinstance(result, dict):
            return result
        timings = dict(state.get("stage_timings") or {})
        timings.update(result.get("stage_timings") or {})
        timings[name] = timings.get(name, 0) + elapsed
        result["stage_timings"] = timings
        return result

    wrapper.__name__ = getattr(node, "__name__", name)
    return wrapper


def build_agent_graph() -> StateGraph:
    """Build the compiled multi-agent state graph."""
    graph = StateGraph(AgentState)

    # Add all agent nodes
    graph.add_node("supervisor", _timed("supervisor", supervisor_node))
    graph.add_node("inventory", _timed("inventory", inventory_agent))
    graph.add_node("booking", _timed("booking", booking_agent))
    graph.add_node("assignment", _timed("assignment", assignment_agent))
    graph.add_node("hitl", _timed("hitl", hitl_agent))
    graph.add_node("respond", _timed("respond", respond_node))

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
    graph.add_conditional_edges("booking", _route_after_worker, {"hitl": "hitl", "respond": "respond"})
    graph.add_conditional_edges("assignment", _route_after_worker, {"hitl": "hitl", "respond": "respond"})
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


@lru_cache
def _trace_callbacks() -> tuple:
    """Langfuse callback for the graph run, built once.

    Returns an empty tuple unless both Langfuse keys are set and the package is
    installed, so tracing stays opt-in and a missing dependency never breaks a
    chat turn.
    """
    from src.config import get_settings

    settings = get_settings()
    if not (settings.langfuse_public_key and settings.langfuse_secret_key):
        return ()
    os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
    os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
    os.environ["LANGFUSE_HOST"] = settings.langfuse_host
    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        logger.warning("Langfuse keys are set but the langfuse package is not installed.")
        return ()
    return (CallbackHandler(),)


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
    callbacks = _trace_callbacks()
    config: dict[str, Any] = {}
    if callbacks:
        # Group every turn of one conversation under the same Langfuse session, and
        # tie it to the customer when signed in, so the dashboard can show a whole
        # chat on one timeline instead of loose per-turn traces.
        config["callbacks"] = list(callbacks)
        config["metadata"] = {
            "langfuse_session_id": state.get("session_id"),
            "langfuse_user_id": state.get("customer_id") or "anonymous",
        }

    try:
        if on_stage is None:
            return await graph.ainvoke(state, config=config)

        merged: dict[str, Any] = dict(state)
        async for chunk in graph.astream(state, stream_mode="updates", config=config):
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
