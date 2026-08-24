import math
from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Appointment, AppointmentStatus


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance between two coordinates in kilometres."""
    earth_radius_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    value = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    return earth_radius_km * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def _local_day_bounds(target_date: date) -> tuple[datetime, datetime]:
    from zoneinfo import ZoneInfo

    local_timezone = ZoneInfo("Asia/Ho_Chi_Minh")
    start = datetime.combine(target_date, time.min, tzinfo=local_timezone)
    return start.astimezone(UTC), (start + timedelta(days=1)).astimezone(UTC)


def _distance(first: Appointment, second: Appointment) -> float:
    return haversine_distance(
        float(first.property.latitude),
        float(first.property.longitude),
        float(second.property.latitude),
        float(second.property.longitude),
    )


def _nearest_neighbour(appointments: list[Appointment]) -> list[Appointment]:
    """Create a stable route without changing any confirmed appointment time."""
    if len(appointments) < 2:
        return appointments

    remaining = appointments[1:]
    ordered = [appointments[0]]
    while remaining:
        current = ordered[-1]
        nearest = min(remaining, key=lambda item: (_distance(current, item), item.starts_at, str(item.id)))
        ordered.append(nearest)
        remaining.remove(nearest)
    return ordered


async def optimize_daily_route(
    db: AsyncSession,
    sale_user_id: UUID,
    date_str: str,
) -> tuple[list[Appointment], float]:
    """Calculate a route for one Sale/day without mutating appointment times."""
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start_utc, end_utc = _local_day_bounds(target_date)

    statement = (
        select(Appointment)
        .where(
            Appointment.sale_user_id == sale_user_id,
            Appointment.starts_at >= start_utc,
            Appointment.starts_at < end_utc,
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
        )
        .options(selectinload(Appointment.property))
        .order_by(Appointment.starts_at, Appointment.id)
    )
    appointments = list((await db.execute(statement)).scalars().all())
    valid = [
        appointment
        for appointment in appointments
        if appointment.property
        and appointment.property.latitude is not None
        and appointment.property.longitude is not None
    ]
    ordered = _nearest_neighbour(valid)
    total_distance = sum(_distance(ordered[index], ordered[index + 1]) for index in range(len(ordered) - 1))
    return ordered, total_distance
