from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import (
    Appointment,
    AppointmentStatus,
    Property,
    RequestStatus,
    TourRequest,
    User,
    UserRole,
    UserStatus,
)
from src.schemas.booking import UserStatusUpdate
from src.services.booking_service import list_all_bookings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview")
async def admin_overview(
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR)),
    db: AsyncSession = Depends(get_session),
):
    users = await db.scalar(select(func.count(User.id))) or 0
    properties = await db.scalar(select(func.count(Property.id))) or 0
    bookings = await db.scalar(select(func.count(TourRequest.id))) or 0
    pending = await db.scalar(
        select(func.count(TourRequest.id)).where(TourRequest.status == RequestStatus.WAITING_APPROVAL)
    ) or 0
    confirmed = await db.scalar(select(func.count(TourRequest.id)).where(TourRequest.status == RequestStatus.BOOKED)) or 0
    no_shows = await db.scalar(select(func.count(Appointment.id)).where(Appointment.status == AppointmentStatus.NO_SHOW)) or 0
    conversion_rate = round(confirmed / bookings * 100, 1) if bookings else 0.0
    return {
        "stats": {
            "users": users,
            "properties": properties,
            "bookings": bookings,
            "pending": pending,
            "conversion_rate": conversion_rate,
            "no_shows": no_shows,
        },
        "recent_bookings": await list_all_bookings(db, limit=20),
    }


@router.get("/users")
async def list_users(
    role: UserRole | None = Query(default=None),
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(User).order_by(User.created_at.desc()).limit(200)
    if role:
        stmt = stmt.where(User.role == role)
    rows = (await db.execute(stmt)).scalars().all()
    return [{
        "id": str(row.id),
        "full_name": row.full_name,
        "email": row.email,
        "phone": row.phone,
        "role": row.role.value,
        "status": row.status.value,
        "last_login_at": row.last_login_at,
        "created_at": row.created_at,
    } for row in rows]


@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: UUID,
    payload: UserStatusUpdate,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Không thể khóa chính tài khoản đang đăng nhập")
    row = await db.get(User, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    try:
        row.status = UserStatus(payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Trạng thái không hợp lệ") from exc
    await db.commit()
    return {"id": str(row.id), "status": row.status.value}
