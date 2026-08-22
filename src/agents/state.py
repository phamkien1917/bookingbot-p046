"""Agent State schema for LangGraph.

This defines the state that flows through the multi-agent graph.
"""

from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    """State schema cho LangGraph multi-agent.

    Mỗi node đọc và ghi vào state này.
    total=False cho phép tất cả fields là optional.
    """

    # ============== Conversation ==============
    query: str  # Current user message
    messages: list[dict]  # Chat history: [{"role": "user", "content": "..."}]
    session_id: str  # Unique session identifier

    # ============== Customer Context ==============
    customer_id: str | None  # Customer UUID
    customer_profile: dict | None  # Cached customer data
    customer_authenticated: bool  # Whether the customer is authenticated
    preferences: list[dict]  # From long-term memory
    preferred_time_slots: list[str]  # e.g., ["weekends", "after_18h"]

    # ============== Booking Context ==============
    current_property_id: str | None  # Property being discussed
    selected_properties: list[dict]  # Properties matching search
    selected_slots: list[dict]  # Proposed time slots
    selected_slot_id: str | None  # User's chosen slot
    booking_in_progress: bool  # Is user in booking flow?
    booking_id: str | None  # Created booking ID

    # ============== Search Criteria ==============
    search_criteria: dict | None  # {
    #     "property_kind": "APARTMENT",
    #     "district": "Quận 7",
    #     "min_price": 2000000000,
    #     "max_price": 4000000000,
    #     "bedrooms": 2,
    #     "features": ["balcony", "parking"]
    # }

    # ============== Agent Routing ==============
    current_agent: str  # conversation | inventory | booking | assignment | hitl
    intent: str | None  # SEARCH | BOOK | CANCEL | RESCHEDULE | INFO
    required_fields: list[str]  # Fields needed for booking
    missing_fields: list[str]  # Fields not yet collected

    # ============== Decision Making ==============
    analysis: str  # LLM's analysis
    confidence: float  # Decision confidence (0.0-1.0)
    next_action: str | None  # Suggested next action

    # ============== Human-in-the-Loop (HITL) ==============
    awaiting_human: bool  # Is workflow paused waiting for human?
    hitl_case_id: str | None  # HITL case identifier
    hitl_reason: str | None  # Why HITL was triggered
    hitl_context: dict | None  # Additional context for human
    human_decision: dict | None  # Human's decision

    # ============== Tool Execution ==============
    tool_calls: list[dict]  # Tools that were called
    tool_results: list[dict]  # Results from tools
    last_tool_error: str | None  # Error from last tool call

    # ============== Response ==============
    response: str  # Final response to user
    suggested_actions: list[str]  # Suggested next user actions

    # ============== Error Handling ==============
    error: str | None  # Any error that occurred
    error_recovery_suggestion: str | None  # How to recover from error

    # ============== Metadata ==============
    metadata: dict  # Additional metadata
    conversation_summary: str | None  # Summary for context window


# ============== Intent Types ==============
class Intent:
    """Defined intent types for routing."""

    SEARCH_PROPERTY = "SEARCH_PROPERTY"
    BOOK_APPOINTMENT = "BOOK_APPOINTMENT"
    CANCEL_BOOKING = "CANCEL_BOOKING"
    RESCHEDULE = "RESCHEDULE"
    GET_INFO = "GET_INFO"
    GENERAL_QA = "GENERAL_QA"  # Câu hỏi tổng quát về BĐS — KHÔNG search DB
    CHECK_STATUS = "CHECK_STATUS"
    GREETING = "GREETING"
    FALLBACK = "FALLBACK"


# ============== Agent Types ==============
class AgentType:
    """Defined agent types."""

    SUPERVISOR = "supervisor"  # Main orchestrator / conversation agent
    INVENTORY = "inventory"  # Property search and suggestions
    BOOKING = "booking"  # Tour request and appointment creation
    ASSIGNMENT = "assignment"  # Sale agent assignment
    HITL = "hitl"  # Human-in-the-loop handling
    RESPOND = "respond"  # Generate final response


# ============== Helper Functions ==============

def create_initial_state(
    session_id: str,
    query: str,
    customer_id: str | None = None,
    customer_role: Any = None,
    history: list[dict] | None = None,
    metadata: dict | None = None,
) -> AgentState:
    """Create initial state for a new conversation.

    Args:
        session_id: Unique session identifier
        query: Initial user message
        customer_id: Customer UUID if authenticated

    Returns:
        Initial AgentState
    """
    msgs = list(history or [])
    if not msgs or msgs[-1].get("content") != query:
        msgs.append({"role": "user", "content": query})

    return AgentState(
        # Conversation
        query=query,
        messages=msgs,
        session_id=session_id,
        # Customer
        customer_id=customer_id,
        customer_profile=None,
        customer_authenticated=customer_id is not None,
        preferences=[],
        preferred_time_slots=[],
        # Booking
        current_property_id=None,
        selected_properties=[],
        selected_slots=[],
        selected_slot_id=None,
        booking_in_progress=False,
        booking_id=None,
        search_criteria=None,
        # Routing
        current_agent=AgentType.SUPERVISOR,
        intent=None,
        required_fields=["property_id", "preferred_time", "customer_info"],
        missing_fields=["property_id", "preferred_time", "customer_info"],
        # Decision
        analysis="",
        confidence=1.0,
        next_action=None,
        # HITL
        awaiting_human=False,
        hitl_case_id=None,
        hitl_reason=None,
        hitl_context=None,
        human_decision=None,
        # Tools
        tool_calls=[],
        tool_results=[],
        last_tool_error=None,
        # Response
        response="",
        suggested_actions=[],
        # Error
        error=None,
        error_recovery_suggestion=None,
        # Metadata
        metadata={},
        conversation_summary=None,
    )


def add_message(state: AgentState, role: str, content: str) -> AgentState:
    """Add a message to the conversation history.

    Args:
        state: Current agent state
        role: Message role (user/assistant/system)
        content: Message content

    Returns:
        Updated state
    """
    messages = state.get("messages", [])
    messages.append({"role": role, "content": content})
    state["messages"] = messages
    return state


def get_conversation_context(
    state: AgentState,
    max_messages: int = 10,
) -> str:
    """Get formatted conversation context for LLM.

    Args:
        state: Current agent state
        max_messages: Maximum messages to include

    Returns:
        Formatted conversation string
    """
    messages = state.get("messages", [])
    recent = messages[-max_messages:] if len(messages) > max_messages else messages

    formatted = []
    for msg in recent:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        formatted.append(f"{role.upper()}: {content}")

    return "\n".join(formatted)
