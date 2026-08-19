from datetime import date, datetime
from uuid import UUID

from src.utils.time import utcnow

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import User, UserRole
from src.schemas.booking import BookingAction, TourRequestCreate
from src.services.booking_service import (
    cancel_customer_booking,
    create_tour_request,
    get_customer_booking,
    get_my_tour_requests,
    list_available_slots,
    reschedule_customer_booking,
    serialize_booking,
)
from src.exceptions import BookingConflictError, BookingNotFoundError, BookingPermissionError

router = APIRouter(prefix="/bookings", tags=["bookings"])


class RescheduleRequest(BaseModel):
    new_preferred_start: datetime
    new_preferred_end: datetime
    sale_user_id: UUID


@router.get("/availability")
async def availability(
    property_id: UUID,
    target_date: date = Query(alias="date"),
    _: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await list_available_slots(db, property_id, target_date)
    except BookingConflictError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("", status_code=201)
async def create_booking(
    request_data: TourRequestCreate,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    try:
        row = await create_tour_request(db, user.id, request_data)
        return serialize_booking(row)
    except BookingConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/my")
async def get_my_bookings(
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    return await get_my_tour_requests(db, user.id)


@router.get("/{booking_id}")
async def get_booking(
    booking_id: UUID,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await get_customer_booking(db, booking_id, user.id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: UUID,
    action: BookingAction,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await cancel_customer_booking(db, booking_id, user.id, action.reason)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{booking_id}/reschedule")
async def reschedule_booking(
    booking_id: UUID,
    payload: RescheduleRequest,
    user: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    """Request rescheduling an existing booking to a new time slot."""
    if payload.new_preferred_start <= utcnow().astimezone(payload.new_preferred_start.tzinfo):
        raise HTTPException(status_code=422, detail="Thời gian bắt đầu mới phải ở tương lai")
    if payload.new_preferred_end <= payload.new_preferred_start:
        raise HTTPException(status_code=422, detail="Thời gian kết thúc phải lớn hơn thời gian bắt đầu")
        
    try:
        result = await reschedule_customer_booking(
            db,
            booking_id,
            user.id,
            payload.sale_user_id,
            payload.new_preferred_start,
            payload.new_preferred_end,
        )
        return result
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except BookingConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

