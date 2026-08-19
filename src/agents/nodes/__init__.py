"""Nodes package for BookingBot AI Agent.

This package contains all the agent nodes for the multi-agent system.
"""

from src.agents.nodes.supervisor import (
    supervisor_node,
    classify_intent,
    route_from_supervisor,
)
from src.agents.nodes.inventory_agent import (
    inventory_agent,
    get_property_details,
)
from src.agents.nodes.booking_agent import (
    booking_agent,
    check_booking_status,
)
from src.agents.nodes.assignment_agent import (
    assignment_agent,
    get_top_sales_for_booking,
    reassign_booking,
)
from src.agents.nodes.hitl_agent import (
    hitl_agent,
    get_pending_hitl_cases,
    get_hitl_case,
    resolve_hitl_case,
)
from src.agents.nodes.respond_node import (
    respond_node,
    format_property_list,
)

__all__ = [
    # Supervisor
    "supervisor_node",
    "classify_intent",
    "route_from_supervisor",
    # Inventory
    "inventory_agent",
    "get_property_details",
    # Booking
    "booking_agent",
    "check_booking_status",
    # Assignment
    "assignment_agent",
    "get_top_sales_for_booking",
    "reassign_booking",
    # HITL
    "hitl_agent",
    "get_pending_hitl_cases",
    "get_hitl_case",
    "resolve_hitl_case",
    # Response
    "respond_node",
    "format_property_list",
]
