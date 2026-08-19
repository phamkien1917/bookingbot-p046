import math
import itertools
from datetime import datetime, timedelta, time
from typing import List
from uuid import UUID

from sqlalchemy import select, and_, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Appointment, AppointmentStatus, Property


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


async def optimize_daily_route(db: AsyncSession, sale_user_id: UUID, date_str: str) -> List[Appointment]:
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    stmt = (
        select(Appointment)
        .where(
            Appointment.sale_user_id == sale_user_id,
            cast(Appointment.starts_at, Date) == target_date,
            Appointment.status.in_([
                AppointmentStatus.WAITING_APPROVAL,
                AppointmentStatus.CONFIRMED,
            ])
        )
        .options(selectinload(Appointment.property))
        .order_by(Appointment.starts_at)
    )
    
    appointments = (await db.execute(stmt)).scalars().all()
    valid_apps = [a for a in appointments if a.property and a.property.latitude and a.property.longitude]
    
    if len(valid_apps) < 2:
        return valid_apps
    
    n = len(valid_apps)
    best_distance = float("inf")
    best_order = valid_apps
    
    for perm in itertools.permutations(valid_apps):
        dist = 0.0
        for i in range(n - 1):
            p1 = perm[i].property
            p2 = perm[i+1].property
            dist += haversine_distance(
                float(p1.latitude), float(p1.longitude),
                float(p2.latitude), float(p2.longitude)
            )
        if dist < best_distance:
            best_distance = dist
            best_order = list(perm)
            
    start_time = datetime.combine(target_date, time(8, 0))
    if valid_apps and valid_apps[0].starts_at:
        min_start = min(a.starts_at.replace(tzinfo=None) for a in valid_apps if a.starts_at)
        start_time = min_start
        
    current_time = start_time
    for apt in best_order:
        apt.starts_at = current_time
        apt.ends_at = current_time + timedelta(hours=1)
        current_time = apt.ends_at + timedelta(minutes=30)
        db.add(apt)
        
    await db.commit()
    return best_order

