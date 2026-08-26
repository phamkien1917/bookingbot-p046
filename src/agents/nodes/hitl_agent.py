"""HITL agent backed by the PostgreSQL coordinator queue."""

from __future__ import annotations

import logging
from uuid import UUID

from src.agents.state import AgentState
from src.database.connection import get_session_context
from src.services.hitl_service import create_hitl_case, get_hitl_case

logger = logging.getLogger(__name__)


def _customer_uuid(state: AgentState) -> UUID | None:
    try:
        return UUID(str(state.get("customer_id"))) if state.get("customer_id") else None
    except ValueError:
        return None


async def hitl_agent(state: AgentState) -> dict:
    """Persist a review request or return its latest durable decision."""
    existing_id = state.get("hitl_case_id")
    async with get_session_context() as db:
        if existing_id:
            try:
                case = await get_hitl_case(db, UUID(str(existing_id)))
            except ValueError:
                case = None
            if case and case.status == "RESOLVED":
                decision = case.decision or {}
                return {
                    "awaiting_human": False,
                    "human_decision": decision,
                    "response": decision.get("message") or "Yêu cầu của bạn đã được điều phối viên xử lý.",
                }
            if case:
                return {
                    "awaiting_human": True,
                    "response": f"Yêu cầu `{case.case_code}` đang chờ điều phối viên xử lý.",
                }

        reason = str(state.get("hitl_reason") or "MANUAL_REVIEW")
        case = await create_hitl_case(
            db,
            reason=reason,
            context=state.get("hitl_context") or {},
            session_id=str(state.get("session_id") or "") or None,
            customer_user_id=_customer_uuid(state),
        )
        logger.info("Durable HITL case created: %s", case.case_code)
        return {
            "awaiting_human": True,
            "hitl_case_id": str(case.id),
            "response": (
                "Yêu cầu cần điều phối viên kiểm tra trước khi tiếp tục. "
                f"Mã xử lý: `{case.case_code}`. Bạn sẽ nhận thông báo ngay khi có quyết định."
            ),
        }
