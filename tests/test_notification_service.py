from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.database.models import Notification
from src.services import notification_service
from src.utils.time import utcnow


@pytest.mark.asyncio
async def test_booking_reminders_are_scheduled_idempotently(monkeypatch) -> None:
    monkeypatch.setattr(notification_service, "_configured_channels", lambda: [])
    appointment = SimpleNamespace(
        id=uuid4(), customer_user_id=uuid4(), booking_code="BK-REMINDER",
        starts_at=utcnow() + timedelta(days=3),
    )
    db = MagicMock()
    db.scalar = AsyncMock(return_value=None)
    added: list[object] = []
    db.add.side_effect = added.append

    created = await notification_service.schedule_booking_reminders(db, appointment, "Căn kiểm thử")

    notifications = [item for item in added if isinstance(item, Notification)]
    assert created == 2
    assert {item.template_key for item in notifications} == {"booking_reminder_24h", "booking_reminder_2h"}
    assert all(item.appointment_id == appointment.id for item in notifications)
