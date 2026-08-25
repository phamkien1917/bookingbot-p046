"""Durable coordinator queue for human-in-the-loop decisions."""

from __future__ import annotations

import uuid
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    DeliveryStatus,
    HitlCase,
    Notification,
    NotificationChannel,
    User,
    UserRole,
    UserStatus,
)
from src.utils.time import utcnow

VALID_DECISIONS = {"APPROVE", "REJECT", "OVERRIDE"}


def serialize_hitl_case(case: HitlCase) -> dict:
    return {
        "id": str(case.id),
        "case_code": case.case_code,
        "reason": case.reason,
        "context": case.context or {},
        "status": case.status,
        "session_id": case.session_id,
        "customer_user_id": str(case.customer_user_id) if case.customer_user_id else None,
        "assigned_coordinator_user_id": (
            str(case.assigned_coordinator_user_id) if case.assigned_coordinator_user_id else None
        ),
        "decision": case.decision or {},
        "expires_at": case.expires_at,
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        "resolved_at": case.resolved_at,
    }


async def create_hitl_case(
    db: AsyncSession,
    *,
    reason: str,
    context: dict | None = None,
    session_id: str | None = None,
    customer_user_id: UUID | None = None,
    expires_minutes: int = 30,
) -> HitlCase:
    case = HitlCase(
        id=uuid.uuid4(),
        case_code=f"HC-{uuid.uuid4().hex[:10].upper()}",
        reason=reason[:100],
        context=context or {},
        status="PENDING",
        session_id=session_id,
        customer_user_id=customer_user_id,
        expires_at=utcnow() + timedelta(minutes=expires_minutes),
    )
    db.add(case)
    await db.flush()

    reviewers = (await db.execute(select(User.id).where(
        User.role.in_([UserRole.COORDINATOR, UserRole.ADMIN]),
        User.status == UserStatus.ACTIVE,
    ))).scalars().all()
    for reviewer_id in reviewers:
        db.add(Notification(
            user_id=reviewer_id,
            channel=NotificationChannel.IN_APP,
            template_key="hitl_case_created",
            payload={"case_id": str(case.id), "case_code": case.case_code, "reason": case.reason},
            status=DeliveryStatus.PENDING,
        ))
    return case


async def get_hitl_case(db: AsyncSession, case_id: UUID) -> HitlCase | None:
    return await db.get(HitlCase, case_id)


async def list_hitl_cases(
    db: AsyncSession,
    *,
    status: str = "PENDING",
    limit: int = 100,
) -> list[dict]:
    query = select(HitlCase).order_by(HitlCase.created_at.asc()).limit(limit)
    if status:
        query = query.where(HitlCase.status == status.upper())
    rows = (await db.execute(query)).scalars().all()
    return [serialize_hitl_case(row) for row in rows]


async def resolve_hitl_case(
    db: AsyncSession,
    case_id: UUID,
    coordinator_user_id: UUID,
    *,
    action: str,
    message: str | None = None,
    metadata: dict | None = None,
) -> HitlCase:
    action = action.upper()
    if action not in VALID_DECISIONS:
        raise ValueError("Quyết định HITL không hợp lệ")
    case = await db.get(HitlCase, case_id, with_for_update=True)
    if not case:
        raise LookupError("Không tìm thấy HITL case")
    if case.status != "PENDING":
        raise ValueError("HITL case đã được xử lý")

    case.status = "RESOLVED"
    case.assigned_coordinator_user_id = coordinator_user_id
    case.resolved_by_user_id = coordinator_user_id
    case.resolved_at = utcnow()
    case.decision = {"action": action, "message": message or "", "metadata": metadata or {}}
    if case.customer_user_id:
        db.add(Notification(
            user_id=case.customer_user_id,
            channel=NotificationChannel.IN_APP,
            template_key="hitl_case_resolved",
            payload={
                "case_id": str(case.id),
                "case_code": case.case_code,
                "action": action,
                "message": message or "",
            },
            status=DeliveryStatus.PENDING,
        ))
    await db.flush()
    return case
