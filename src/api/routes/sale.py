import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import (
    Appointment,
    AppointmentStatus,
    Property,
    PropertyHold,
    PropertySaleAssignment,
    SaleProfile,
    User,
    UserRole,
)
from src.schemas.booking import BookingAction
from src.services.analytics_service import record_event
from src.services.booking_service import (
    accept_sale_request,
    list_sale_requests,
    reject_sale_request,
)
from src.services.property_hold_service import extend_property_hold, release_appointment_hold
from src.services.route_optimizer import optimize_daily_route_plan
from src.utils.time import utcnow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sale", tags=["sale"])


class HoldExtensionRequest(BaseModel):
    minutes: int | None = Field(default=None, ge=1, le=120)


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


@router.get("/sale-profiles/me")
async def get_my_sale_profile(
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(SaleProfile).where(SaleProfile.user_id == user.id)
    profile = (await db.execute(stmt)).scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Sale profile not found")
    return profile


@router.post("/optimize-route")
async def optimize_route(
    date: str,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    """Build a time-window and traffic-aware itinerary for a Sale/day."""
    try:
        plan = await optimize_daily_route_plan(db, user.id, date)
        return {
            "message": "Route optimized successfully",
            "count": len(plan.appointments),
            "appointment_ids": [str(appointment.id) for appointment in plan.appointments],
            "total_distance_km": round(plan.total_distance_km, 2),
            "total_duration_minutes": plan.total_duration_minutes,
            "provider": plan.provider,
            "traffic_aware": plan.traffic_aware,
            "feasible": plan.feasible,
            "legs": plan.legs,
            "warnings": plan.warnings,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Error checking sale availability")
        raise HTTPException(status_code=500, detail="Đã xảy ra lỗi khi kiểm tra lịch trống. Vui lòng thử lại sau.")


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


@router.post("/appointments/{appointment_id}/hold/extend")
async def extend_hold(
    appointment_id: UUID,
    payload: HoldExtensionRequest,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    if appointment.sale_user_id != user.id:
        raise HTTPException(status_code=403, detail="Lịch hẹn không thuộc về bạn")
    hold = await db.scalar(select(PropertyHold).where(PropertyHold.appointment_id == appointment_id))
    if not hold:
        raise HTTPException(status_code=404, detail="Lịch hẹn chưa có lượt giữ căn")
    try:
        updated = await extend_property_hold(db, hold.id, user.id, minutes=payload.minutes)
        return {"id": str(updated.id), "hold_code": updated.hold_code, "expires_at": updated.expires_at}
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/appointments/{appointment_id}/hold/release")
async def release_hold(
    appointment_id: UUID,
    action: BookingAction,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    if appointment.sale_user_id != user.id:
        raise HTTPException(status_code=403, detail="Lịch hẹn không thuộc về bạn")
    hold = await release_appointment_hold(db, appointment_id, action.reason or "SALE_RELEASED")
    return {"released": hold is not None, "hold_id": str(hold.id) if hold else None}


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
    complete: bool = False,
):
    """Helper to update an appointment's status, verifying sale ownership."""
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")
    if appointment.sale_user_id != sale_user_id:
        raise HTTPException(status_code=403, detail="Lịch hẹn không thuộc về bạn")
    if check_in:
        appointment.checked_in_at = utcnow()
    if complete:
        appointment.checked_out_at = utcnow()
    appointment.status = new_status
    record_event(
        db,
        f"appointment_{new_status.value.lower()}",
        customer_user_id=appointment.customer_user_id,
        appointment_id=appointment.id,
        properties={"sale_user_id": str(sale_user_id)},
    )
    await db.commit()
    return {
        "id": str(appointment.id),
        "status": new_status.value if hasattr(new_status, "value") else new_status,
        "checked_in_at": appointment.checked_in_at.isoformat() if appointment.checked_in_at else None,
        "checked_out_at": appointment.checked_out_at.isoformat() if appointment.checked_out_at else None,
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
    return await _update_appointment_status(
        db, appointment_id, user.id, AppointmentStatus.COMPLETED, complete=True
    )


@router.post("/properties/{property_id}/verify")
async def verify_property_listing(
    property_id: UUID,
    user: User = Depends(require_roles(UserRole.SALE)),
    db: AsyncSession = Depends(get_session),
):
    """Sale confirms the listing is still live, resetting its freshness clock."""
    assigned = await db.scalar(
        select(PropertySaleAssignment.property_id).where(
            PropertySaleAssignment.property_id == property_id,
            PropertySaleAssignment.sale_user_id == user.id,
            PropertySaleAssignment.unassigned_at.is_(None),
        )
    )
    if not assigned:
        raise HTTPException(status_code=403, detail="Bạn không phụ trách căn này")

    prop = await db.get(Property, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy căn")

    prop.last_verified_at = utcnow()
    record_event(
        db,
        "property_verified",
        properties={"property_id": str(property_id), "sale_user_id": str(user.id)},
    )
    await db.commit()
    return {
        "id": str(prop.id),
        "code": prop.code,
        "last_verified_at": prop.last_verified_at.isoformat(),
    }

