"""Agent State schema for LangGraph Multi-Agent System.

This defines the state that flows through all nodes in the agent graph.
"""

from __future__ import annotations

from typing import Any, TypedDict

from src.database.models import UserRole


# ============== Intent Constants ==============
class Intent:
    SEARCH_PROPERTY = "SEARCH_PROPERTY"
    SELECT_PROPERTY = "SELECT_PROPERTY"
    PROPERTY_DETAILS = "PROPERTY_DETAILS"
    COMPARE_PROPERTIES = "COMPARE_PROPERTIES"
    BOOK_APPOINTMENT = "BOOK_APPOINTMENT"
    SELECT_SLOT = "SELECT_SLOT"
    CHECK_STATUS = "CHECK_STATUS"
    CANCEL_BOOKING = "CANCEL_BOOKING"
    RESCHEDULE = "RESCHEDULE"
    CONFIRM = "CONFIRM"
    DENY = "DENY"
    CONSULTATION_QA = "CONSULTATION_QA"
    GREETING = "GREETING"
    THANKS = "THANKS"
    GOODBYE = "GOODBYE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    FALLBACK = "FALLBACK"


# ============== Agent Type Constants ==============
class AgentType:
    SUPERVISOR = "supervisor"
    INVENTORY = "inventory"
    BOOKING = "booking"
    ASSIGNMENT = "assignment"
    HITL = "hitl"
    RESPOND = "respond"


class AgentState(TypedDict, total=False):
    """Full AgentState flowing through LangGraph nodes."""

    # ============== Conversation & Context ==============
    query: str  # Current user message
    messages: list[dict[str, Any]]  # Chat history: [{"role": "user"|"assistant", "content": "..."}]
    session_id: str  # Conversation session UUID
    customer_id: str | None  # Customer UUID if logged in
    customer_role: UserRole | None  # Role of customer
    customer_authenticated: bool  # True if user is logged in as CUSTOMER

    # ============== Search & Recommendations ==============
    search_criteria: dict[str, Any]  # {district, province, property_kind, min_price, max_price, min_bedrooms, min_bathrooms, min_area}
    soft_preferences: list[str]  # e.g. ["yên tĩnh", "gần trường học", "view thoáng", "ban công"]
    household_context: list[str]  # e.g. ["gia đình 4 người", "có con nhỏ", "nuôi thú cưng"]
    commute_landmark: str | None  # e.g. "Quận 1", "Sân bay Tân Sơn Nhất"
    max_commute_minutes: int | None
    max_commute_km: float | None
    travel_mode: str  # DRIVE, WALK, BICYCLE, TRANSIT, TWO_WHEELER
    nearby_categories: list[str]
    user_location: dict[str, float] | None  # Ephemeral; never persisted to conversation memory
    monthly_income_vnd: int | None  # Income the customer stated, used to derive a price ceiling
    own_capital_vnd: int | None  # Savings the customer stated; changes the ceiling a lot
    affordability_note: str | None  # Deterministic explanation of how the ceiling was derived
    selected_properties: list[dict[str, Any]]  # Full property items matching search / current view
    search_results: list[dict[str, Any]]  # Preserved list of search result properties across turns
    current_property_id: str | None  # ID of property being discussed / selected
    selected_property_index: int | None  # 0-indexed number of selected property
    comparison_properties: list[dict[str, Any]]  # Properties for side-by-side comparison

    # ============== Booking & Scheduling ==============
    requested_date: str | None  # Target date (YYYY-MM-DD)
    invalid_requested_date: bool  # User explicitly supplied a past/invalid date
    requested_hour: int | None  # Target hour (0-23)
    selected_slots: list[dict[str, Any]]  # Available slots proposed to customer
    selected_slot_index: int | None  # 0-indexed slot chosen by customer
    active_request_id: str | None  # TourRequest / Appointment UUID
    active_request_code: str | None  # Code like TR-XXXXX or BK-XXXXX
    pending_action: str | None  # Workflow flag (e.g. "CREATE_BOOKING", "CANCEL_CONFIRMATION", "RESCHEDULE:uuid")
    phase: str  # Phase: IDLE, SEARCH_RESULTS, PROPERTY_SELECTED, AWAITING_DATE, AWAITING_SLOT, AWAITING_AUTH, AWAITING_CANCEL_CONFIRMATION, WAITING_APPROVAL
    auth_required: bool  # Whether customer must sign in to proceed

    # ============== Routing & Understanding ==============
    current_agent: str  # supervisor | inventory | booking | assignment | hitl | respond
    intent: str | None  # Classification from Intent constants
    confidence: float  # Classification confidence
    direct_response: str | None  # Pre-generated direct response from LLM
    analysis: str  # Internal reasoning notes

    # ============== HITL (Human-in-the-Loop) ==============
    awaiting_human: bool
    hitl_case_id: str | None
    hitl_reason: str | None
    hitl_context: dict[str, Any] | None
    human_decision: dict[str, Any] | None

    # ============== Final Response & Metadata ==============
    response: str  # Final text output in Markdown
    response_kind: str  # SEARCH_RESULTS, PROPERTY_ADVICE, DIRECT, OUT_OF_SCOPE, etc.
    suggested_actions: list[str]  # Quick reply chips
    insights: dict[str, Any]  # Accumulated criteria & preferences
    memory_summary: str  # Long term customer memory summary
    ai_mode: str  # llm_grounded, llm_direct, llm_intent, fallback
    ai_model: str | None
    ai_latency_ms: int
    error: str | None


def create_initial_agent_state(
    session_id: str,
    query: str,
    customer_id: str | None = None,
    customer_role: UserRole | None = None,
    history: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
    memory_summary: str = "",
) -> AgentState:
    """Create a fully initialized AgentState from session and metadata."""
    stored_state = (metadata or {}).get("chat_state", {})

    state: AgentState = {
        "query": query,
        "messages": list(history or []),
        "session_id": session_id,
        "customer_id": customer_id,
        "customer_role": customer_role,
        "customer_authenticated": customer_id is not None and customer_role == UserRole.CUSTOMER,
        "search_criteria": stored_state.get("criteria", {}),
        "soft_preferences": stored_state.get("soft_preferences", []),
        "household_context": stored_state.get("household_context", []),
        "commute_landmark": stored_state.get("commute_landmark"),
        "max_commute_minutes": stored_state.get("max_commute_minutes"),
        "max_commute_km": stored_state.get("max_commute_km"),
        "travel_mode": stored_state.get("travel_mode", "DRIVE"),
        "nearby_categories": stored_state.get("nearby_categories", []),
        "user_location": None,
        "monthly_income_vnd": stored_state.get("monthly_income_vnd"),
        "own_capital_vnd": stored_state.get("own_capital_vnd"),
        "affordability_note": None,
        "selected_properties": stored_state.get("property_refs", []),
        "search_results": stored_state.get("search_result_refs", stored_state.get("property_refs", [])),
        "current_property_id": stored_state.get("selected_property_id"),
        "selected_property_index": stored_state.get("selected_property_index"),
        "comparison_properties": [],
        "requested_date": stored_state.get("requested_date"),
        "invalid_requested_date": False,
        "requested_hour": stored_state.get("requested_hour"),
        "selected_slots": stored_state.get("slots", []),
        "selected_slot_index": stored_state.get("selected_slot_index"),
        "active_request_id": stored_state.get("active_request_id"),
        "active_request_code": stored_state.get("active_request_code"),
        "pending_action": stored_state.get("pending_action"),
        "phase": stored_state.get("phase", "IDLE"),
        "auth_required": False,
        "current_agent": AgentType.SUPERVISOR,
        "intent": None,
        "confidence": 1.0,
        "direct_response": None,
        "analysis": "",
        "awaiting_human": False,
        "hitl_case_id": None,
        "hitl_reason": None,
        "hitl_context": None,
        "human_decision": None,
        "response": "",
        "response_kind": "DIRECT",
        "suggested_actions": [],
        "insights": (metadata or {}).get("insights", {}),
        "memory_summary": memory_summary or stored_state.get("memory_summary", ""),
        "ai_mode": "llm_grounded",
        "ai_model": None,
        "ai_latency_ms": 0,
        "error": None,
    }
    return state
