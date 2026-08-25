import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Appointment, AppointmentStatus
from src.services.geo_service import get_geo_service


@dataclass
class RoutePlan:
    appointments: list[Appointment]
    total_distance_km: float
    total_duration_minutes: float | None
    provider: str
    traffic_aware: bool
    feasible: bool
    legs: list[dict]
    warnings: list[str]


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
    """Backward-compatible route result used by older callers."""
    plan = await optimize_daily_route_plan(db, sale_user_id, date_str)
    return plan.appointments, plan.total_distance_km


async def optimize_daily_route_plan(
    db: AsyncSession,
    sale_user_id: UUID,
    date_str: str,
) -> RoutePlan:
    """Build a traffic-aware itinerary while respecting confirmed time windows."""
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
    # Confirmed appointments have fixed time windows. Reordering them for a
    # shorter geometric path can make the schedule impossible, so chronology is
    # the primary constraint and route evidence validates each transition.
    ordered = sorted(valid, key=lambda item: (item.starts_at, item.id))
    geo = get_geo_service()
    legs: list[dict] = []
    warnings: list[str] = []
    total_distance = 0.0
    total_duration = 0.0
    all_grounded = geo.configured and len(ordered) > 1
    now = datetime.now(UTC)

    for index in range(len(ordered) - 1):
        origin, destination = ordered[index], ordered[index + 1]
        evidence = None
        if geo.configured:
            try:
                matrix = await geo.route_matrix(
                    [(float(origin.property.latitude), float(origin.property.longitude))],
                    (float(destination.property.latitude), float(destination.property.longitude)),
                    "DRIVE",
                    departure_time=max(origin.ends_at, now),
                )
                evidence = matrix.get(0)
            except Exception:
                all_grounded = False
        if evidence:
            distance_km = float(evidence["distance_km"])
            duration_minutes = float(evidence["duration_minutes"])
            total_duration += duration_minutes
        else:
            all_grounded = False
            distance_km = _distance(origin, destination)
            duration_minutes = None
        total_distance += distance_km
        available_minutes = (destination.starts_at - origin.ends_at).total_seconds() / 60
        feasible = duration_minutes is None or duration_minutes <= available_minutes
        if not feasible:
            warnings.append(
                f"Không đủ thời gian đi từ {origin.booking_code} đến {destination.booking_code}: "
                f"cần {duration_minutes:.0f} phút nhưng chỉ có {max(available_minutes, 0):.0f} phút."
            )
        legs.append({
            "from_appointment_id": str(origin.id),
            "to_appointment_id": str(destination.id),
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_minutes, 1) if duration_minutes is not None else None,
            "available_minutes": round(available_minutes, 1),
            "feasible": feasible,
        })

    return RoutePlan(
        appointments=ordered,
        total_distance_km=total_distance,
        total_duration_minutes=total_duration if all_grounded else None,
        provider=(
            "NO_ROUTE_NEEDED" if len(ordered) < 2
            else "Google Routes" if all_grounded
            else "HAVERSINE_FALLBACK"
        ),
        traffic_aware=all_grounded and geo.settings.geo_traffic_aware,
        feasible=not warnings,
        legs=legs,
        warnings=warnings,
    )
