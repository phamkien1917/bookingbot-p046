"""HITL (Human-in-the-Loop) Agent - Handles cases requiring human intervention."""

import logging
import uuid
from datetime import datetime, timedelta

from src.agents.state import AgentState

logger = logging.getLogger(__name__)


# HITL Case Storage (in production, this would be in database)
_hitl_cases: dict = {}


async def hitl_agent(state: AgentState) -> dict:
    """HITL agent - handles cases requiring human intervention.

    This agent:
    1. Pauses the workflow
    2. Creates a HITL case for admin review
    3. Notifies admin (in production, via webhook/notification)
    4. Waits for human decision

    Args:
        state: Current agent state

    Returns:
        Updated state with HITL information
    """
    await_human = state.get("awaiting_human", False)
    hitl_case_id = state.get("hitl_case_id")

    # If already awaiting human decision, check if it's been made
    if await_human and hitl_case_id:
        return await _check_human_decision(state, hitl_case_id)

    # Create new HITL case
    return await _create_hitl_case(state)


async def _create_hitl_case(state: AgentState) -> dict:
    """Create a new HITL case.

    Args:
        state: Current agent state

    Returns:
        Updated state with HITL case
    """
    hitl_reason = state.get("hitl_reason")
    hitl_context = state.get("hitl_context", {})

    # Generate case ID
    case_id = str(uuid.uuid4())

    # Create case record
    case = {
        "id": case_id,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat(),
        "reason": hitl_reason,
        "context": hitl_context,
        "status": "PENDING",
        "decision": None,
        "session_id": state.get("session_id"),
        "customer_id": state.get("customer_id"),
    }

    # Store case
    _hitl_cases[case_id] = case

    logger.info(f"HITL case created: {case_id} - Reason: {hitl_reason}")

    # Generate user-facing message
    response = _generate_hitl_message(hitl_reason, case_id)

    return {
        "awaiting_human": True,
        "hitl_case_id": case_id,
        "response": response,
        "analysis": f"HITL case created: {case_id}",
    }


async def _check_human_decision(state: AgentState, case_id: str) -> dict:
    """Check if human has made a decision on the HITL case.

    Args:
        state: Current agent state
        case_id: HITL case ID

    Returns:
        Updated state with decision or waiting message
    """
    case = _hitl_cases.get(case_id)

    if not case:
        logger.warning(f"HITL case not found: {case_id}")
        return {
            "awaiting_human": False,
            "hitl_case_id": None,
            "response": "Trường hợp của bạn đang được xử lý. Chúng tôi sẽ liên hệ sớm nhất.",
        }

    # Check if decision has been made
    if case.get("decision"):
        logger.info(f"HITL case resolved: {case_id}")

        decision = case["decision"]
        action = decision.get("action")

        # Process the decision
        if action == "APPROVE":
            return {
                "awaiting_human": False,
                "hitl_case_id": None,
                "human_decision": decision,
                "response": decision.get("message", "Yêu cầu của bạn đã được xử lý thành công!"),
            }
        elif action == "REJECT":
            return {
                "awaiting_human": False,
                "hitl_case_id": None,
                "human_decision": decision,
                "response": decision.get("message", "Yêu cầu của bạn không thể được xử lý lúc này. Vui lòng thử lại sau."),
            }
        elif action == "OVERRIDE":
            return {
                "awaiting_human": False,
                "hitl_case_id": None,
                "human_decision": decision,
                "response": decision.get("message", "Yêu cầu của bạn đã được xử lý với sự can thiệp của quản lý."),
            }
        else:
            return {
                "awaiting_human": False,
                "hitl_case_id": None,
                "human_decision": decision,
                "response": "Yêu cầu của bạn đang được xử lý.",
            }

    # Still waiting for decision
    return {
        "awaiting_human": True,
        "hitl_case_id": case_id,
        "response": _get_waiting_message(case.get("reason")),
    }


def _generate_hitl_message(reason: str, case_id: str) -> str:
    """Generate user-facing message for HITL case.

    Args:
        reason: HITL reason code
        case_id: Case ID

    Returns:
        User-facing message
    """
    messages = {
        "NO_SALE_AVAILABLE": (
            "Hiện tại tất cả sale đều đang bận hoặc không có sale phụ trách khu vực này. "
            "Nhân viên quản lý sẽ xem xét và phân công phù hợp nhất cho bạn.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
        "ASSIGNMENT_FAILED": (
            "Gặp sự cố khi phân công sale cho booking của bạn. "
            "Nhân viên quản lý sẽ xử lý và liên hệ với bạn trong giây lát.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
        "ASSIGNMENT_ERROR": (
            "Đã xảy ra lỗi trong quá trình xử lý. "
            "Nhân viên quản lý sẽ kiểm tra và liên hệ với bạn sớm nhất.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
        "BOOKING_CONFLICT": (
            "Lịch bạn yêu cầu đang bị xung đột với các booking khác. "
            "Nhân viên quản lý sẽ đề xuất lịch thay thế phù hợp nhất.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
        "VIP_CUSTOMER": (
            "Yêu cầu của bạn cần được xác nhận bởi quản lý do là khách VIP. "
            "Chúng tôi sẽ xử lý ưu tiên cho bạn.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
        "HIGH_VALUE_TRANSACTION": (
            "Đây là giao dịch có giá trị cao, cần được xác nhận bởi quản lý. "
            "Chúng tôi sẽ xử lý nhanh nhất có thể.\n\n"
            f"Mã yêu cầu: `{case_id}`"
        ),
    }

    return messages.get(
        reason,
        f"Yêu cầu của bạn đang được nhân viên quản lý xem xét. "
        f"Chúng tôi sẽ liên hệ lại trong giây lát.\n\nMã yêu cầu: `{case_id}`"
    )


def _get_waiting_message(reason: str) -> str:
    """Get waiting message for pending HITL case.

    Args:
        reason: HITL reason code

    Returns:
        Waiting message
    """
    return (
        "Yêu cầu của bạn vẫn đang được xử lý bởi nhân viên quản lý. "
        "Vui lòng đợi trong giây lát hoặc chúng tôi sẽ liên hệ với bạn sớm nhất.\n\n"
        "Bạn có thể:\n"
        "- Đợi để được xử lý tự động\n"
        "- Liên hệ trực tiếp qua hotline\n"
        "- Hoặc yêu cầu hỗ trợ khác"
    )


# Admin API functions

def get_pending_hitl_cases() -> list[dict]:
    """Get all pending HITL cases.

    Returns:
        List of pending HITL cases
    """
    return [
        {
            "id": case["id"],
            "created_at": case["created_at"],
            "expires_at": case["expires_at"],
            "reason": case["reason"],
            "context": case["context"],
            "status": case["status"],
            "session_id": case["session_id"],
            "customer_id": case["customer_id"],
        }
        for case in _hitl_cases.values()
        if case["status"] == "PENDING"
    ]


def get_hitl_case(case_id: str) -> dict | None:
    """Get a specific HITL case.

    Args:
        case_id: Case ID

    Returns:
        HITL case or None
    """
    return _hitl_cases.get(case_id)


def resolve_hitl_case(
    case_id: str,
    decision: dict,
) -> dict:
    """Resolve a HITL case with a decision.

    Args:
        case_id: Case ID
        decision: Decision dict {
            "action": "APPROVE" | "REJECT" | "OVERRIDE",
            "message": str,
            "metadata": dict
        }

    Returns:
        Result dict
    """
    case = _hitl_cases.get(case_id)

    if not case:
        return {"error": "Case not found"}

    if case["status"] != "PENDING":
        return {"error": "Case already resolved"}

    case["status"] = "RESOLVED"
    case["resolved_at"] = datetime.utcnow().isoformat()
    case["decision"] = decision

    logger.info(f"HITL case resolved: {case_id} - Action: {decision.get('action')}")

    return {
        "success": True,
        "case_id": case_id,
        "action": decision.get("action"),
    }
