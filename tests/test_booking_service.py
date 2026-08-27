import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from src.database.models import User, UserRole, UserStatus, Appointment, AppointmentStatus
from src.services.booking_service import get_available_slots, reject_sale_request


@pytest.mark.asyncio
async def test_booking_available_slots_empty_property(db_session):
    """Test getting available slots for a property with no existing appointments."""
    property_id = uuid4()
    date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    slots = await get_available_slots(db_session, property_id, date_str)
    assert isinstance(slots, list)
    # Typically 08:00 to 18:00 means several slots
    assert len(slots) > 0


@pytest.mark.asyncio
async def test_reject_sale_request(db_session):
    """Test rejecting a booking request."""
    # This requires an actual appointment in the DB
    sale_user = User(
        email="sale.reject.test@example.com",
        full_name="Sale User",
        password_hash="test",
        role=UserRole.SALE,
        status=UserStatus.ACTIVE,
    )
    db_session.add(sale_user)
    await db_session.flush()

    appt = Appointment(
        booking_code="TESTREJ",
        property_id=uuid4(),
        customer_user_id=uuid4(),
        sale_user_id=sale_user.id,
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=1),
        status=AppointmentStatus.WAITING_APPROVAL
    )
    db_session.add(appt)
    await db_session.commit()

    # Reject it
    result = await reject_sale_request(db_session, appt.id, sale_user.id, "Busy")
    assert result["status"] == "CANCELLED"

    # Verify status in DB
    from sqlalchemy import select
    appt_db = (await db_session.execute(select(Appointment).where(Appointment.id == appt.id))).scalar_one()
    assert appt_db.status == AppointmentStatus.CANCELLED
