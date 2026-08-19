"""Tools package for BookingBot AI Agent.

This package contains all the function-calling tools that agents can use.
"""

from src.agents.tools.property_tools import (
    search_properties,
    check_property_availability,
    hold_property,
    release_hold,
)

from src.agents.tools.booking_tools import (
    calculate_viewing_time,
    create_booking,
    propose_time_slots,
    get_booking_status,
    cancel_booking,
)

from src.agents.tools.assignment_tools import (
    calculate_assignment_score,
    assign_sale_to_booking,
    get_available_sales,
    check_sale_availability,
)

# All available tools
ALL_TOOLS = [
    # Property tools
    search_properties,
    check_property_availability,
    hold_property,
    release_hold,
    # Booking tools
    calculate_viewing_time,
    create_booking,
    propose_time_slots,
    get_booking_status,
    cancel_booking,
    # Assignment tools
    calculate_assignment_score,
    assign_sale_to_booking,
    get_available_sales,
    check_sale_availability,
]

__all__ = [
    # Property tools
    "search_properties",
    "check_property_availability",
    "hold_property",
    "release_hold",
    # Booking tools
    "calculate_viewing_time",
    "create_booking",
    "propose_time_slots",
    "get_booking_status",
    "cancel_booking",
    # Assignment tools
    "calculate_assignment_score",
    "assign_sale_to_booking",
    "get_available_sales",
    "check_sale_availability",
    # All tools
    "ALL_TOOLS",
]
