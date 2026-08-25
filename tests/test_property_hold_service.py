from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.database.models import HoldStatus
from src.exceptions import BookingConflictError
from src.services.property_hold_service import create_hold_for_appointment
from src.utils.time import utcnow


@pytest.mark.asyncio
async def test_hold_uses_real_appointment_foreign_keys() -> None:
    appointment = SimpleNamespace(
        id=uuid4(), property_id=uuid4(), customer_user_id=uuid4(), sale_user_id=uuid4()
    )
    db = MagicMock()
    db.execute = AsyncMock()
    db.scalar = AsyncMock(side_effect=[None, None])
    db.flush = AsyncMock()

    hold = await create_hold_for_appointment(db, appointment, appointment.sale_user_id, hold_minutes=15)

    assert hold.appointment_id == appointment.id
    assert hold.property_id == appointment.property_id
    assert hold.customer_user_id == appointment.customer_user_id
    assert hold.approved_by_user_id == appointment.sale_user_id
    assert hold.status == HoldStatus.ACTIVE
    assert hold.expires_at > utcnow()
    db.add.assert_called_once_with(hold)


@pytest.mark.asyncio
async def test_hold_rejects_another_active_property_hold() -> None:
    appointment = SimpleNamespace(
        id=uuid4(), property_id=uuid4(), customer_user_id=uuid4(), sale_user_id=uuid4()
    )
    active = SimpleNamespace(status=HoldStatus.ACTIVE, expires_at=utcnow() + timedelta(minutes=5))
    db = MagicMock()
    db.execute = AsyncMock()
    db.scalar = AsyncMock(side_effect=[None, active])
    db.flush = AsyncMock()

    with pytest.raises(BookingConflictError, match="đang được giữ"):
        await create_hold_for_appointment(db, appointment, appointment.sale_user_id)

    db.add.assert_not_called()
