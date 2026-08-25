"""Transactional property holds backed by real appointments.

A hold never manufactures placeholder booking, sale, or approval identifiers.  It
can only be created for an appointment that already passed the sale approval
workflow.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database.models import Appointment, HoldStatus, PropertyHold
from src.exceptions import BookingConflictError, BookingNotFoundError
from src.utils.time import utcnow


async def create_hold_for_appointment(
    db: AsyncSession,
    appointment: Appointment,
    approved_by_user_id: UUID,
    *,
    hold_minutes: int | None = None,
) -> PropertyHold:
    """Create one race-safe active hold for a confirmed appointment."""
    minutes = hold_minutes or get_settings().hold_default_minutes
    if minutes < 1:
        raise ValueError("hold_minutes must be positive")

    await db.execute(
        text("SELECT pg_advisory_xact_lock(hashtext(:key))"),
        {"key": f"property-hold:{appointment.property_id}"},
    )
    now = utcnow()

    existing_for_appointment = await db.scalar(
        select(PropertyHold).where(PropertyHold.appointment_id == appointment.id)
    )
    if existing_for_appointment:
        if existing_for_appointment.status == HoldStatus.ACTIVE and existing_for_appointment.expires_at > now:
            return existing_for_appointment
        raise BookingConflictError("Lịch hẹn này đã có một lần giữ căn trước đó")

    active = await db.scalar(
        select(PropertyHold).where(
            PropertyHold.property_id == appointment.property_id,
            PropertyHold.status == HoldStatus.ACTIVE,
        )
    )
    if active and active.expires_at <= now:
        active.status = HoldStatus.EXPIRED
        active.released_at = now
        active.release_reason = "AUTO_EXPIRED_ON_CREATE"
        await db.flush()
        active = None
    if active:
        raise BookingConflictError(
            f"Căn đang được giữ bởi yêu cầu khác đến {active.expires_at.isoformat()}"
        )

    expires_at = now + timedelta(minutes=minutes)
    hold = PropertyHold(
        id=uuid.uuid4(),
        hold_code=f"HD{uuid.uuid4().hex[:8].upper()}",
        appointment_id=appointment.id,
        property_id=appointment.property_id,
        customer_user_id=appointment.customer_user_id,
        approved_by_user_id=approved_by_user_id,
        status=HoldStatus.ACTIVE,
        starts_at=now,
        expires_at=expires_at,
        max_expires_at=expires_at + timedelta(minutes=minutes * get_settings().max_hold_extensions),
        extension_count=0,
    )
    db.add(hold)
    await db.flush()
    return hold


async def release_appointment_hold(
    db: AsyncSession,
    appointment_id: UUID,
    reason: str,
) -> PropertyHold | None:
    hold = await db.scalar(
        select(PropertyHold).where(
            PropertyHold.appointment_id == appointment_id,
            PropertyHold.status == HoldStatus.ACTIVE,
        )
    )
    if not hold:
        return None
    hold.status = HoldStatus.RELEASED
    hold.released_at = utcnow()
    hold.release_reason = reason[:500]
    await db.flush()
    return hold


async def extend_property_hold(
    db: AsyncSession,
    hold_id: UUID,
    approved_by_user_id: UUID,
    *,
    minutes: int | None = None,
) -> PropertyHold:
    """Extend a hold within its configured hard limit."""
    hold = await db.get(PropertyHold, hold_id, with_for_update=True)
    if not hold:
        raise BookingNotFoundError("Không tìm thấy lượt giữ căn")
    now = utcnow()
    if hold.status != HoldStatus.ACTIVE or hold.expires_at <= now:
        raise BookingConflictError("Lượt giữ căn đã hết hiệu lực")
    if hold.extension_count >= get_settings().max_hold_extensions:
        raise BookingConflictError("Lượt giữ căn đã đạt số lần gia hạn tối đa")
    extension = timedelta(minutes=minutes or get_settings().hold_default_minutes)
    new_expiry = min(hold.expires_at + extension, hold.max_expires_at)
    if new_expiry <= hold.expires_at:
        raise BookingConflictError("Lượt giữ căn đã đạt thời hạn tối đa")
    hold.expires_at = new_expiry
    hold.extension_count += 1
    hold.approved_by_user_id = approved_by_user_id
    await db.flush()
    return hold
