from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.database.models import RequestStatus, SlotStatus
from src.exceptions import BookingConflictError, BookingPermissionError
from src.services import booking_service
from src.services.booking_service import (
    reject_sale_request,
)


def _booking(status, slot_options):
    return SimpleNamespace(
        id=uuid4(),
        status=status,
        slot_options=slot_options,
        extracted_requirements=None,
    )


@pytest.mark.asyncio
async def test_reject_refuses_booking_no_longer_waiting(monkeypatch) -> None:
    """A booking already approved or cancelled must not be rejectable again."""
    booking = _booking(RequestStatus.APPROVED, [])

    async def fake_get_booking(db, booking_id):
        return booking

    monkeypatch.setattr(booking_service, "_get_booking", fake_get_booking)

    with pytest.raises(BookingConflictError):
        await reject_sale_request(MagicMock(), booking.id, uuid4(), "Busy")


@pytest.mark.asyncio
async def test_reject_refuses_sale_without_selected_slot(monkeypatch) -> None:
    """Only the sale holding the SELECTED slot may reject the request."""
    other_sale = uuid4()
    booking = _booking(
        RequestStatus.WAITING_APPROVAL,
        [SimpleNamespace(sale_user_id=other_sale, status=SlotStatus.SELECTED)],
    )

    async def fake_get_booking(db, booking_id):
        return booking

    monkeypatch.setattr(booking_service, "_get_booking", fake_get_booking)

    with pytest.raises(BookingPermissionError):
        await reject_sale_request(MagicMock(), booking.id, uuid4(), "Busy")


@pytest.mark.asyncio
async def test_reject_withdraws_slot_and_records_reason(monkeypatch) -> None:
    """Rejecting withdraws the sale's slot and keeps the reason on the request."""
    sale_user_id = uuid4()
    slot = SimpleNamespace(sale_user_id=sale_user_id, status=SlotStatus.SELECTED)
    booking = _booking(RequestStatus.WAITING_APPROVAL, [slot])

    async def fake_get_booking(db, booking_id):
        return booking

    async def fake_reassign(db, row, trigger):
        return False

    async def fake_notify(db, row, kind, message):
        return None

    monkeypatch.setattr(booking_service, "_get_booking", fake_get_booking)
    monkeypatch.setattr(booking_service, "_reassign_waiting_request", fake_reassign)
    monkeypatch.setattr(booking_service, "_notify_customer_and_operators", fake_notify)
    monkeypatch.setattr(booking_service, "serialize_booking", lambda row: {"status": row.status})

    db = MagicMock()
    db.commit = AsyncMock()

    result = await reject_sale_request(db, booking.id, sale_user_id, "Kẹt lịch")

    assert slot.status == SlotStatus.WITHDRAWN
    assert booking.extracted_requirements["rejection_reason"] == "Kẹt lịch"
    assert booking.status == RequestStatus.REJECTED
    assert result["status"] == RequestStatus.REJECTED
