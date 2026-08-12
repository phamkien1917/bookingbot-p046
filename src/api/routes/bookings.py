from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
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
    serialize_booking,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/availability")
async def availability(
    property_id: UUID,
    target_date: date = Query(alias="date"),
    _: User = Depends(require_roles(UserRole.CUSTOMER)),
    db: AsyncSession = Depends(get_session),
):
    try:
        return await list_available_slots(db, property_id, target_date)
    except ValueError as exc:
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
    except ValueError as exc:
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
    except LookupError as exc:
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
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
