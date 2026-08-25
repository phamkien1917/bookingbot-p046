"""Conflict recovery that proposes alternatives without mutating a booking."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import (
    Appointment,
    DeliveryStatus,
    Notification,
    NotificationChannel,
    RescheduleProposal,
)
from src.exceptions import BookingConflictError, BookingNotFoundError
from src.services.analytics_service import record_event
from src.services.booking_service import list_available_slots, reschedule_customer_booking
from src.utils.time import utcnow


def serialize_proposal(row: RescheduleProposal) -> dict:
    return {
        "id": str(row.id),
        "appointment_id": str(row.appointment_id),
        "sale_user_id": str(row.proposed_sale_user_id),
        "starts_at": row.proposed_start.isoformat(),
        "ends_at": row.proposed_end.isoformat(),
        "status": row.status,
        "reason": row.reason,
        "expires_at": row.expires_at.isoformat(),
    }


async def propose_alternative_slots(
    db: AsyncSession,
    appointment_id: UUID,
    customer_user_id: UUID,
    *,
    desired_start: datetime | None = None,
    reason: str = "SCHEDULE_CONFLICT",
    limit: int = 3,
) -> list[dict]:
    appointment = await db.scalar(
        select(Appointment)
        .options(selectinload(Appointment.property))
        .where(Appointment.id == appointment_id)
    )
    if not appointment or appointment.customer_user_id != customer_user_id:
        raise BookingNotFoundError("Không tìm thấy lịch hẹn")

    await db.execute(
        update(RescheduleProposal)
        .where(
            RescheduleProposal.appointment_id == appointment_id,
            RescheduleProposal.status == "PENDING",
        )
        .values(status="SUPERSEDED", decided_at=utcnow())
    )

    anchor = desired_start or (appointment.starts_at + timedelta(days=1))
    candidates: list[dict] = []
    for day_offset in range(0, 8):
        target_date = (anchor + timedelta(days=day_offset)).date()
        availability = await list_available_slots(
            db,
            appointment.property_id,
            target_date,
            customer_user_id=customer_user_id,
        )
        for slot in availability.get("slots", []):
            start = datetime.fromisoformat(slot["starts_at"])
            if start <= utcnow().astimezone(start.tzinfo):
                continue
            candidates.append(slot)
        if len(candidates) >= limit:
            break

    if not candidates:
        raise BookingConflictError("Không tìm thấy khung giờ thay thế trong 8 ngày tới")

    candidates.sort(key=lambda slot: (
        0 if slot.get("preference_match") else 1,
        abs((datetime.fromisoformat(slot["starts_at"]) - anchor).total_seconds()),
    ))
    expires_at = utcnow() + timedelta(minutes=30)
    proposals: list[RescheduleProposal] = []
    for slot in candidates[:limit]:
        proposal = RescheduleProposal(
            appointment_id=appointment.id,
            customer_user_id=customer_user_id,
            proposed_sale_user_id=UUID(slot["sale_user_id"]),
            proposed_start=datetime.fromisoformat(slot["starts_at"]),
            proposed_end=datetime.fromisoformat(slot["ends_at"]),
            status="PENDING",
            reason=reason,
            expires_at=expires_at,
        )
        db.add(proposal)
        proposals.append(proposal)
    await db.flush()

    db.add(Notification(
        user_id=customer_user_id,
        appointment_id=appointment.id,
        channel=NotificationChannel.IN_APP,
        template_key="reschedule_alternatives_ready",
        payload={"proposal_ids": [str(item.id) for item in proposals], "reason": reason},
        status=DeliveryStatus.PENDING,
    ))
    record_event(
        db,
        "reschedule_alternatives_proposed",
        customer_user_id=customer_user_id,
        appointment_id=appointment.id,
        properties={"count": len(proposals), "reason": reason},
    )
    return [serialize_proposal(item) for item in proposals]


async def confirm_reschedule_proposal(
    db: AsyncSession,
    proposal_id: UUID,
    customer_user_id: UUID,
) -> dict:
    proposal = await db.get(RescheduleProposal, proposal_id, with_for_update=True)
    if not proposal or proposal.customer_user_id != customer_user_id:
        raise BookingNotFoundError("Không tìm thấy đề xuất dời lịch")
    if proposal.status != "PENDING" or proposal.expires_at <= utcnow():
        raise BookingConflictError("Đề xuất dời lịch đã hết hiệu lực")
    appointment = await db.get(Appointment, proposal.appointment_id)
    if not appointment:
        raise BookingNotFoundError("Không tìm thấy lịch hẹn gốc")

    result = await reschedule_customer_booking(
        db,
        appointment.tour_request_id,
        customer_user_id,
        proposal.proposed_sale_user_id,
        proposal.proposed_start,
        proposal.proposed_end,
    )
    proposal.status = "CONFIRMED"
    proposal.decided_at = utcnow()
    await db.execute(
        update(RescheduleProposal)
        .where(
            RescheduleProposal.appointment_id == proposal.appointment_id,
            RescheduleProposal.id != proposal.id,
            RescheduleProposal.status == "PENDING",
        )
        .values(status="REJECTED", decided_at=utcnow())
    )
    record_event(
        db,
        "reschedule_alternative_confirmed",
        customer_user_id=customer_user_id,
        appointment_id=appointment.id,
        properties={"proposal_id": str(proposal.id)},
    )
    return result


async def reject_reschedule_proposal(
    db: AsyncSession,
    proposal_id: UUID,
    customer_user_id: UUID,
) -> dict:
    proposal = await db.get(RescheduleProposal, proposal_id, with_for_update=True)
    if not proposal or proposal.customer_user_id != customer_user_id:
        raise BookingNotFoundError("Không tìm thấy đề xuất dời lịch")
    if proposal.status != "PENDING":
        raise BookingConflictError("Đề xuất không còn chờ xác nhận")
    proposal.status = "REJECTED"
    proposal.decided_at = utcnow()
    return serialize_proposal(proposal)
