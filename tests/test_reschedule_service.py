from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.services import reschedule_service
from src.utils.time import utcnow


@pytest.mark.asyncio
async def test_proposals_do_not_mutate_original_appointment(monkeypatch) -> None:
    original_status = "CONFIRMED"
    appointment = SimpleNamespace(
        id=uuid4(),
        tour_request_id=uuid4(),
        customer_user_id=uuid4(),
        property_id=uuid4(),
        starts_at=utcnow() + timedelta(days=2),
        status=original_status,
        property=SimpleNamespace(title="Test property"),
    )
    candidate_start = utcnow() + timedelta(days=3)

    async def fake_availability(*args, **kwargs):
        return {"slots": [{
            "sale_user_id": str(uuid4()),
            "starts_at": candidate_start.isoformat(),
            "ends_at": (candidate_start + timedelta(hours=1)).isoformat(),
            "preference_match": True,
        }]}

    monkeypatch.setattr(reschedule_service, "list_available_slots", fake_availability)
    db = MagicMock()
    db.scalar = AsyncMock(return_value=appointment)
    db.execute = AsyncMock()
    db.flush = AsyncMock()

    proposals = await reschedule_service.propose_alternative_slots(
        db, appointment.id, appointment.customer_user_id, limit=1
    )

    assert len(proposals) == 1
    assert proposals[0]["status"] == "PENDING"
    assert appointment.status == original_status
    assert proposals[0]["starts_at"] == candidate_start.isoformat()
