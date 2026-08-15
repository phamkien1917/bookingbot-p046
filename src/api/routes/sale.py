from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import (
    Appointment,
    AppointmentStatus,
    User,
    UserRole,
)
from src.schemas.booking import BookingAction
from src.services.booking_service import (
    accept_sale_request,
    list_sale_requests,
    reject_sale_request,
)

router = APIRouter(prefix="/sale", tags=["sale"])


@router.get("/overview")
async def sale_overview(
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    requests = await list_sale_requests(db, user.id)
    pending = [row for row in requests if row["status"] == "WAITING_APPROVAL"]
    confirmed = [row for row in requests if row["status"] == "BOOKED"]
    return {
        "user": {"id": str(user.id), "full_name": user.full_name},
        "stats": {"pending": len(pending), "confirmed": len(confirmed)},
        "pending_requests": pending,
        "schedule": confirmed,
    }


@router.get("/schedule")
async def sale_schedule(
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    """Return all appointments for the sale agent with full time details for calendar view."""
    stmt = (
        select(Appointment)
        .where(Appointment.sale_user_id == user.id)
        .where(Appointment.status.in_([
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.IN_PROGRESS,
            AppointmentStatus.COMPLETED,
            AppointmentStatus.NO_SHOW,
        ]))
        .options(selectinload(Appointment.property))
        .order_by(Appointment.starts_at)
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(a.id),
            "booking_code": a.booking_code,
            "status": a.status.value if hasattr(a.status, "value") else a.status,
            "starts_at": a.starts_at.isoformat() if a.starts_at else None,
            "ends_at": a.ends_at.isoformat() if a.ends_at else None,
            "customer_user_id": str(a.customer_user_id),
            "customer_note": a.customer_note,
            "checked_in_at": a.checked_in_at.isoformat() if a.checked_in_at else None,
            "property": {
                "id": str(a.property.id),
                "title": a.property.title,
                "address": ", ".join(filter(None, [a.property.address_line, a.property.district, a.property.province])),
                "latitude": float(a.property.latitude) if a.property.latitude else None,
                "longitude": float(a.property.longitude) if a.property.longitude else None,
            } if a.property else None,
        }
        for a in rows
    ]


@router.post("/requests/{booking_id}/accept")
async def accept_request(
    booking_id: UUID,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await accept_sale_request(db, booking_id, user.id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/requests/{booking_id}/reject")
async def reject_request(
    booking_id: UUID,
    action: BookingAction,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await reject_sale_request(db, booking_id, user.id, action.reason)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


async def _update_appointment_status(
    db: AsyncSession,
    appointment_id: UUID,
    sale_user_id: UUID,
    new_status: AppointmentStatus,
    *,
    check_in: bool = False,
):
    """Helper to update an appointment's status, verifying sale ownership."""
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    if appointment.sale_user_id != sale_user_id:
        raise HTTPException(status_code=403, detail="Lịch hẹn không thuộc về bạn")
    if check_in:
        appointment.checked_in_at = datetime.utcnow()
    appointment.status = new_status
    await db.commit()
    return {
        "id": str(appointment.id),
        "status": new_status.value,
        "checked_in_at": appointment.checked_in_at.isoformat() if appointment.checked_in_at else None,
    }


@router.post("/appointments/{appointment_id}/check-in")
async def check_in_appointment(
    appointment_id: UUID,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    return await _update_appointment_status(
        db, appointment_id, user.id, AppointmentStatus.IN_PROGRESS, check_in=True
    )


@router.post("/appointments/{appointment_id}/no-show")
async def mark_no_show(
    appointment_id: UUID,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    return await _update_appointment_status(
        db, appointment_id, user.id, AppointmentStatus.NO_SHOW
    )


@router.post("/appointments/{appointment_id}/complete")
async def complete_appointment(
    appointment_id: UUID,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    if appointment.sale_user_id != user.id:
        raise HTTPException(status_code=403, detail="Lịch hẹn không thuộc về bạn")
    appointment.status = AppointmentStatus.COMPLETED
    appointment.checked_out_at = datetime.utcnow()
    await db.commit()
    return {"id": str(appointment.id), "status": "COMPLETED"}

