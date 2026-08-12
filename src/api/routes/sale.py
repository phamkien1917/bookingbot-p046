from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import User, UserRole
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
