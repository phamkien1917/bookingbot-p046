"""Conditional routing: which node the graph hands a turn to next.

Routing is the one part of the agent with no model in the loop — it is plain
Python reading state — so it is also the part that can be pinned exactly. When a
recommendation comes out wrong the first question is which node produced it, and
that answer is only trustworthy if routing itself is known good.

Two decisions live here:

  * `route_from_supervisor` picks the worker for a turn
  * `_route_after_worker` decides whether a worker's result still needs a human
"""

import pytest

from src.agents.graph import _route_after_worker, build_agent_graph
from src.agents.nodes.supervisor import route_from_supervisor
from src.agents.state import AgentType

WORKERS = [
    AgentType.INVENTORY,
    AgentType.BOOKING,
    AgentType.ASSIGNMENT,
    AgentType.HITL,
    AgentType.RESPOND,
]


def graph_nodes() -> set[str]:
    """The graph's own nodes, minus LangGraph's __start__ sentinel."""
    return {name for name in build_agent_graph().nodes if not name.startswith("__")}


class TestRouteFromSupervisor:
    """The supervisor writes `current_agent`; routing only reads it back."""

    @pytest.mark.parametrize("current_agent", WORKERS)
    def test_every_worker_is_reachable(self, current_agent):
        assert route_from_supervisor({"current_agent": current_agent}) == current_agent

    def test_an_unset_agent_answers_instead_of_crashing(self):
        """A supervisor that wrote nothing must still produce a reply."""
        assert route_from_supervisor({}) == AgentType.RESPOND

    @pytest.mark.parametrize("current_agent", WORKERS)
    def test_every_destination_exists_in_the_graph(self, current_agent):
        """A route to a node the graph does not define fails at runtime.

        LangGraph resolves the branch map when the turn is already in flight, so
        a missing entry surfaces as a broken conversation rather than a startup
        error. Checking it here turns that into a build failure.
        """
        assert current_agent in graph_nodes()


class TestRouteAfterWorker:
    """The gate that stops a machine confirming on a person's behalf."""

    @pytest.mark.parametrize(
        "state,expected",
        [
            ({"awaiting_human": True}, "hitl"),
            ({"awaiting_human": False}, "respond"),
            ({}, "respond"),
            ({"awaiting_human": None}, "respond"),
        ],
    )
    def test_only_an_explicit_flag_reaches_a_human(self, state, expected):
        assert _route_after_worker(state) == expected

    def test_a_finished_looking_state_does_not_skip_the_gate(self):
        """A worker that produced a full answer can still need approval.

        Booking writes a reply and sets awaiting_human in the same step; routing
        past hitl because a response already exists would confirm a tour that no
        sale ever saw.
        """
        state = {
            "awaiting_human": True,
            "response": "Đã tìm được khung giờ phù hợp.",
            "properties": [{"id": "x"}],
        }

        assert _route_after_worker(state) == "hitl"


def test_the_graph_has_exactly_the_six_nodes_it_documents():
    """docs/architecture_diagram.md draws six; a seventh would make it wrong."""
    assert graph_nodes() == {
        "supervisor",
        "inventory",
        "booking",
        "assignment",
        "hitl",
        "respond",
    }
