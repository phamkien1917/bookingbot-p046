import uuid
from datetime import timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Date, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.routes.auth import require_roles
from src.database import get_session
from src.database.models import (
    Appointment,
    AppointmentStatus,
    Property,
    PropertyKind,
    PropertyStatus,
    RequestStatus,
    SaleProfile,
    TourRequest,
    User,
    UserRole,
    UserStatus,
)
from src.schemas.admin import PropertyCreate, PropertyUpdate, SaleProfileUpdate
from src.schemas.booking import UserStatusUpdate
from src.services.booking_service import list_all_bookings
from src.utils.time import utcnow

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


@router.get("/analytics")
async def admin_analytics(
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR)),
    db: AsyncSession = Depends(get_session),
):
    """Return analytics data for admin dashboard charts."""
    from sqlalchemy import case
    today = utcnow().astimezone(ZoneInfo("Asia/Ho_Chi_Minh")).date()
    start_date = today - timedelta(days=28)  # 4 weeks ago

    # --- Batch Daily & Weekly bookings ---
    # We can fetch the last 28 days of data in one query, then group in memory
    req_stmt = select(
        cast(TourRequest.created_at, Date).label("day"),
        func.count(TourRequest.id).label("total"),
        func.count(case((TourRequest.status == RequestStatus.BOOKED, 1))).label("confirmed"),
        func.count(case((TourRequest.status.in_([RequestStatus.CANCELLED, RequestStatus.REJECTED]), 1))).label("cancelled")
    ).where(
        cast(TourRequest.created_at, Date) >= start_date,
        cast(TourRequest.created_at, Date) <= today
    ).group_by(cast(TourRequest.created_at, Date))
    req_result = await db.execute(req_stmt)
    req_stats = {row.day: {"total": row.total, "confirmed": row.confirmed, "cancelled": row.cancelled} for row in req_result.all()}

    # No-shows
    apt_stmt = select(
        cast(Appointment.starts_at, Date).label("day"),
        func.count(Appointment.id).label("no_show")
    ).where(
        cast(Appointment.starts_at, Date) >= start_date,
        cast(Appointment.starts_at, Date) <= today,
        Appointment.status == AppointmentStatus.NO_SHOW
    ).group_by(cast(Appointment.starts_at, Date))
    apt_result = await db.execute(apt_stmt)
    apt_stats = {row.day: row.no_show for row in apt_result.all()}

    daily = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        r = req_stats.get(day, {"total": 0, "confirmed": 0, "cancelled": 0})
        no_show_count = apt_stats.get(day, 0)
        daily.append({
            "date": day.isoformat(),
            "total": r["total"],
            "confirmed": r["confirmed"],
            "cancelled": r["cancelled"],
            "no_show": no_show_count,
        })

    weekly = []
    for week_offset in range(3, -1, -1):
        week_end = today - timedelta(days=week_offset * 7)
        week_start = week_end - timedelta(days=7)

        week_total = sum(req_stats.get(week_start + timedelta(days=i), {}).get("total", 0) for i in range(7))
        week_confirmed = sum(req_stats.get(week_start + timedelta(days=i), {}).get("confirmed", 0) for i in range(7))
        rate = round(week_confirmed / week_total * 100, 1) if week_total else 0.0

        weekly.append({
            "week_label": f"{week_start.strftime('%d/%m')} – {(week_end - timedelta(days=1)).strftime('%d/%m')}",
            "total": week_total,
            "confirmed": week_confirmed,
            "rate": rate,
        })

    # --- Status distribution ---
    # Single query for all request statuses
    dist_stmt = select(
        TourRequest.status,
        func.count(TourRequest.id)
    ).group_by(TourRequest.status)
    dist_result = await db.execute(dist_stmt)

    dist = {k.lower(): 0 for k in ["BOOKED", "WAITING_APPROVAL", "CANCELLED", "REJECTED", "EXPIRED"]}
    for status_val, count in dist_result.all():
        key = status_val.value.lower() if hasattr(status_val, 'value') else str(status_val).lower()
        if key in dist:
            dist[key] = count

    no_shows_total = await db.scalar(
        select(func.count(Appointment.id)).where(Appointment.status == AppointmentStatus.NO_SHOW)
    ) or 0
    dist["no_show"] = no_shows_total

    return {
        "daily_bookings": daily,
        "status_distribution": dist,
        "weekly_conversion": weekly,
    }


@router.get("/properties")
async def list_properties(
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR)),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Property).order_by(Property.created_at.desc())
    if q:
        stmt = stmt.where(Property.title.ilike(f"%{q}%"))

    total = await db.scalar(select(func.count(Property.id)).select_from(stmt.subquery()))
    stmt = stmt.limit(limit).offset(offset)

    rows = (await db.execute(stmt)).scalars().all()
    return {
        "items": [{
            "id": str(p.id),
            "code": p.code,
            "title": p.title,
            "property_kind": p.property_kind.value,
            "status": p.status.value,
            "area_sqm": float(p.area_sqm),
            "list_price": float(p.list_price) if p.list_price else None,
            "address": f"{p.address_line}, {p.district}, {p.province}",
            "bedrooms": p.bedrooms,
            "bathrooms": p.bathrooms,
            "created_at": p.created_at,
        } for p in rows],
        "total": total or 0
    }




@router.post("/properties")
async def create_property(
    payload: PropertyCreate,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    code = f"P{uuid.uuid4().hex[:6].upper()}"
    prop = Property(
        code=code,
        title=payload.title,
        property_kind=PropertyKind(payload.property_kind),
        area_sqm=payload.area_sqm,
        list_price=payload.list_price,
        address_line=payload.address_line,
        province=payload.province,
        district=payload.district,
        ward=payload.ward,
        bedrooms=payload.bedrooms,
        bathrooms=payload.bathrooms,
        status=PropertyStatus(payload.status),
        description=payload.description,
    )
    db.add(prop)
    await db.commit()
    return {"id": str(prop.id), "code": code}

@router.patch("/properties/{property_id}")
async def update_property(
    property_id: UUID,
    payload: PropertyUpdate,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    prop = await db.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Không tìm thấy BĐS")

    update_data = payload.model_dump(exclude_unset=True)
    if "property_kind" in update_data:
        update_data["property_kind"] = PropertyKind(update_data["property_kind"])
    if "status" in update_data:
        update_data["status"] = PropertyStatus(update_data["status"])

    for k, v in update_data.items():
        setattr(prop, k, v)

    await db.commit()
    return {"id": str(prop.id)}




@router.get("/sales")
async def list_sales(
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR)),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(User).options(selectinload(User.sale_profile)).where(User.role == UserRole.SALE)
    rows = (await db.execute(stmt)).scalars().all()

    return [{
        "id": str(u.id),
        "full_name": u.full_name,
        "email": u.email,
        "phone": u.phone,
        "status": u.status.value,
        "employee_code": u.sale_profile.employee_code if u.sale_profile else None,
        "job_title": u.sale_profile.job_title if u.sale_profile else None,
        "branch_name": u.sale_profile.branch_name if u.sale_profile else None,
        "max_daily_tours": u.sale_profile.max_daily_tours if u.sale_profile else 0,
        "is_accepting_tours": u.sale_profile.is_accepting_tours if u.sale_profile else False,
    } for u in rows]

@router.patch("/sales/{user_id}")
async def update_sale_profile(
    user_id: UUID,
    payload: SaleProfileUpdate,
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    profile = await db.get(SaleProfile, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy Sale profile")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(profile, k, v)

    await db.commit()
    return {"id": str(profile.user_id)}
