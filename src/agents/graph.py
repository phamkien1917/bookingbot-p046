"""Main LangGraph workflow for BookingBot AI Agent.

This file defines the multi-agent graph with supervisor-workers architecture.
"""

import logging
from typing import Literal

from langgraph.graph import END, StateGraph

from src.agents.state import AgentState, AgentType
from src.agents.nodes import (
    supervisor_node,
    route_from_supervisor,
    inventory_agent,
    booking_agent,
    assignment_agent,
    hitl_agent,
    respond_node,
)

logger = logging.getLogger(__name__)


def should_continue(state: AgentState) -> Literal["supervisor", "inventory", "booking", "assignment", "hitl", "respond", "__end__"]:
    """Determine the next node based on current state.

    This is the main routing function that decides which node to execute next.

    Args:
        state: Current agent state

    Returns:
        Next node name or END
    """
    # If there's an error, go to respond to deliver error message
    if state.get("error") and state.get("response"):
        return "respond"

    # If awaiting human decision, continue with HITL
    if state.get("awaiting_human"):
        return "hitl"

    # Use the supervisor's routing logic
    next_node = route_from_supervisor(state)

    # Validate next node
    valid_nodes = ["supervisor", "inventory", "booking", "assignment", "hitl", "respond", "__end__"]
    if next_node not in valid_nodes:
        logger.warning(f"Invalid next node: {next_node}, defaulting to respond")
        return "respond"

    return next_node


def build_agent_graph() -> StateGraph:
    """Build the multi-agent state graph.

    Graph Structure:
    ┌─────────────┐
    │  SUPERVISOR │ (Entry point - classifies intent)
    └──────┬──────┘
           │
    ┌──────┼──────┐
    │      │      │
    ▼      ▼      ▼
┌──────┐ ┌─────┐ ┌──────────┐
│  IN- │ │BOOK-│ │RESPOND   │◄───(for simple responses)
│VENTORY│ │ING  │ │          │
└──┬───┘ └──┬──┘ └──────────┘
   │        │
   │        ▼
   │   ┌──────────┐
   │   │ASSIGNMENT│
   │   └────┬─────┘
   │        │
   │        ▼
   │   ┌─────────┐
   └──►│ HITL    │ (if needed)
       └────┬────┘
            │
            ▼
       ┌──────────┐
       │ RESPOND  │
       └──────────┘

    Returns:
        Compiled StateGraph
    """
    graph = StateGraph(AgentState)

    # Add all nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("inventory", inventory_agent)
    graph.add_node("booking", booking_agent)
    graph.add_node("assignment", assignment_agent)
    graph.add_node("hitl", hitl_agent)
    graph.add_node("respond", respond_node)

    # Set entry point
    graph.set_entry_point("supervisor")

    # Add conditional edges from supervisor
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "inventory": "inventory",
            "booking": "booking",
            "assignment": "assignment",
            "hitl": "hitl",
            "respond": "respond",
        }
    )

    # Direct edges from specialized agents to respond
    graph.add_edge("inventory", "respond")
    graph.add_edge("respond", END)

    # Booking can lead to assignment
    graph.add_edge("booking", "assignment")

    # Assignment leads to respond or hitl
    def assignment_router(state: AgentState) -> str:
        if state.get("awaiting_human"):
            return "hitl"
        return "respond"

    graph.add_conditional_edges(
        "assignment",
        assignment_router,
        {
            "hitl": "hitl",
            "respond": "respond",
        }
    )

    # HITL always leads to respond (which checks for decisions)
    graph.add_edge("hitl", "respond")

    # Compile the graph
    return graph.compile()


def build_simple_graph() -> StateGraph:
    """Build a simpler graph for basic functionality testing.

    Returns:
        Compiled StateGraph
    """
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("respond", respond_node)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "inventory": "respond",  # Shortcut for MVP
            "booking": "respond",    # Shortcut for MVP
            "respond": "respond",
        }
    )

    graph.add_edge("respond", END)

    return graph.compile()


# Create singleton instances
_agent_graph = None
_simple_graph = None


def get_agent_graph() -> StateGraph:
    """Get the main agent graph.

    Returns:
        Compiled StateGraph
    """
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph


def get_simple_graph() -> StateGraph:
    """Get the simple graph for testing.

    Returns:
        Compiled StateGraph
    """
    global _simple_graph
    if _simple_graph is None:
        _simple_graph = build_simple_graph()
    return _simple_graph


# Main graph instance
agent = get_agent_graph()


# For backwards compatibility
def get_agent() -> StateGraph:
    """Get the agent graph (backwards compatibility)."""
    return agent
