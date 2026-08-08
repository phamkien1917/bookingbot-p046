import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from uuid import UUID

from src.database.models import TourRequest, Appointment, PropertyHold
from src.schemas.booking import TourRequestCreate


async def create_tour_request(db: AsyncSession, customer_user_id: UUID, data: TourRequestCreate):
    """
    Tạo một yêu cầu xem nhà (Tour Request).
    """
    # Generate unique request code
    short_uuid = str(uuid.uuid4()).replace("-", "")[:12].upper()
    request_code = f"TR-{short_uuid}"

    new_request = TourRequest(
        request_code=request_code,
        customer_user_id=customer_user_id,
        property_id=data.property_id,
        preferred_start=data.preferred_start,
        preferred_end=data.preferred_end,
        party_size=data.pax_count,
        customer_note=data.customer_note,
        status='DRAFT'
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request


async def get_my_tour_requests(db: AsyncSession, customer_user_id: UUID):
    """
    Lấy danh sách các yêu cầu xem nhà của khách hàng.
    """
    stmt = select(TourRequest).where(
        TourRequest.customer_user_id == customer_user_id
    ).order_by(TourRequest.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def execute_soft_hold(db: AsyncSession, appointment_id: UUID, approved_by_user_id: UUID, hold_minutes: int = 30):
    """
    Calls the built-in PostgreSQL function create_property_hold()
    which performs a row-level lock (SELECT FOR UPDATE) and prevents concurrent holds.
    """
    stmt = text("""
        SELECT * FROM create_property_hold(
            :appointment_id, 
            :approved_by_user_id, 
            :hold_minutes::smallint
        )
    """)
    result = await db.execute(stmt, {
        "appointment_id": str(appointment_id),
        "approved_by_user_id": str(approved_by_user_id),
        "hold_minutes": hold_minutes
    })
    row = result.fetchone()
    await db.commit()
    return row
