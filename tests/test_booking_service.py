from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.database.models import AppointmentStatus, PropertyStatus, RequestStatus, SlotStatus
from src.exceptions import BookingConflictError, BookingNotFoundError, BookingPermissionError
from src.schemas.booking import TourRequestCreate
from src.services import booking_service
from src.services.booking_service import (
    cancel_customer_booking,
    create_tour_request,
    reject_sale_request,
)
from src.utils.time import utcnow


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


def _create_payload(**overrides):
    start = utcnow() + timedelta(days=1)
    payload = {
        "property_id": uuid4(),
        "sale_user_id": uuid4(),
        "preferred_start": start,
        "preferred_end": start + timedelta(hours=1),
        "pax_count": 2,
    }
    payload.update(overrides)
    return TourRequestCreate(**payload)


def _create_db(prop, sale, conflict_counts):
    """AsyncSession stub for create_tour_request: get() -> property then sale."""
    db = MagicMock()
    db.get = AsyncMock(side_effect=[prop, sale])
    db.execute = AsyncMock()
    db.scalar = AsyncMock(side_effect=list(conflict_counts))
    db.flush = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_create_refuses_property_that_is_not_available() -> None:
    """A sold or under-offer property must not accept new tour requests."""
    prop = SimpleNamespace(id=uuid4(), status=PropertyStatus.SOLD, title="Nhà đã bán")
    sale = SimpleNamespace(is_accepting_tours=True)

    with pytest.raises(BookingConflictError):
        await create_tour_request(_create_db(prop, sale, []), uuid4(), _create_payload())


@pytest.mark.asyncio
async def test_create_refuses_sale_not_accepting_tours() -> None:
    prop = SimpleNamespace(id=uuid4(), status=PropertyStatus.AVAILABLE, title="Căn hộ")
    sale = SimpleNamespace(is_accepting_tours=False)

    with pytest.raises(BookingConflictError):
        await create_tour_request(_create_db(prop, sale, []), uuid4(), _create_payload())


@pytest.mark.asyncio
async def test_create_refuses_slot_in_the_past() -> None:
    """The time window is validated against now, not only against itself."""
    prop = SimpleNamespace(id=uuid4(), status=PropertyStatus.AVAILABLE, title="Căn hộ")
    sale = SimpleNamespace(is_accepting_tours=True)
    past = utcnow() - timedelta(days=1)
    payload = _create_payload(preferred_start=past, preferred_end=past + timedelta(hours=1))

    with pytest.raises(BookingConflictError):
        await create_tour_request(_create_db(prop, sale, []), uuid4(), payload)


@pytest.mark.asyncio
async def test_create_refuses_window_already_confirmed_for_that_sale() -> None:
    """Double booking: the sale already has a confirmed appointment overlapping."""
    prop = SimpleNamespace(id=uuid4(), status=PropertyStatus.AVAILABLE, title="Căn hộ")
    sale = SimpleNamespace(is_accepting_tours=True)
    db = _create_db(prop, sale, [1])

    with pytest.raises(BookingConflictError):
        await create_tour_request(db, uuid4(), _create_payload())

    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_refuses_window_held_by_a_pending_request() -> None:
    """No confirmed appointment yet, but another request still holds the slot."""
    prop = SimpleNamespace(id=uuid4(), status=PropertyStatus.AVAILABLE, title="Căn hộ")
    sale = SimpleNamespace(is_accepting_tours=True)
    db = _create_db(prop, sale, [0, 1])

    with pytest.raises(BookingConflictError):
        await create_tour_request(db, uuid4(), _create_payload())

    db.flush.assert_not_awaited()


def _cancellable(customer_id, status=RequestStatus.WAITING_APPROVAL, appointment=None, slots=None):
    return SimpleNamespace(
        id=uuid4(),
        request_code="TR-TEST",
        customer_user_id=customer_id,
        status=status,
        appointment=appointment,
        slot_options=slots if slots is not None else [],
        property=SimpleNamespace(title="Căn hộ Cầu Giấy"),
    )


def _patch_cancel_deps(monkeypatch, row):
    async def fake_get_booking(db, booking_id):
        return row

    monkeypatch.setattr(booking_service, "_get_booking", fake_get_booking)
    monkeypatch.setattr(booking_service, "serialize_booking", lambda r: {"status": r.status})
    db = MagicMock()
    db.commit = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_cancel_refuses_a_booking_owned_by_someone_else(monkeypatch) -> None:
    """Guessing a booking id must not let another customer cancel it."""
    row = _cancellable(uuid4())
    db = _patch_cancel_deps(monkeypatch, row)

    with pytest.raises(BookingNotFoundError):
        await cancel_customer_booking(db, row.id, uuid4(), "Đổi ý")

    assert row.status == RequestStatus.WAITING_APPROVAL


@pytest.mark.asyncio
async def test_cancel_is_idempotent_on_an_already_cancelled_booking(monkeypatch) -> None:
    """Cancelling twice must not add a second notification for the sale."""
    customer_id = uuid4()
    row = _cancellable(customer_id, status=RequestStatus.CANCELLED)
    db = _patch_cancel_deps(monkeypatch, row)

    result = await cancel_customer_booking(db, row.id, customer_id, "Đổi ý")

    assert result["status"] == RequestStatus.CANCELLED
    db.add.assert_not_called()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_cancel_withdraws_slots_and_notifies_the_selected_sale(monkeypatch) -> None:
    """Request with no appointment yet: the sale holding the slot is told."""
    customer_id = uuid4()
    sale_user_id = uuid4()
    slot = SimpleNamespace(sale_user_id=sale_user_id, status=SlotStatus.SELECTED)
    row = _cancellable(customer_id, slots=[slot])
    db = _patch_cancel_deps(monkeypatch, row)

    await cancel_customer_booking(db, row.id, customer_id, "Bận việc")

    assert row.status == RequestStatus.CANCELLED
    assert slot.status == SlotStatus.WITHDRAWN
    notification = db.add.call_args[0][0]
    assert notification.user_id == sale_user_id
    assert notification.payload["reason"] == "Bận việc"
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_cancel_releases_the_hold_of_a_confirmed_appointment(monkeypatch) -> None:
    """A confirmed booking must free its property hold, not just flip a status."""
    customer_id = uuid4()
    appointment = SimpleNamespace(
        id=uuid4(),
        sale_user_id=uuid4(),
        status=AppointmentStatus.CONFIRMED,
        cancelled_at=None,
        cancellation_reason=None,
    )
    row = _cancellable(customer_id, appointment=appointment)
    db = _patch_cancel_deps(monkeypatch, row)

    released = []
    monkeypatch.setattr(
        booking_service,
        "release_appointment_hold",
        AsyncMock(side_effect=lambda db, appointment_id, reason: released.append(reason)),
    )
    monkeypatch.setattr(booking_service, "cancel_appointment_notifications", AsyncMock())

    await cancel_customer_booking(db, row.id, customer_id, None)

    assert released == ["BOOKING_CANCELLED"]
    assert appointment.status == AppointmentStatus.CANCELLED
    assert appointment.cancellation_reason == "Khách hàng yêu cầu hủy"
    assert row.status == RequestStatus.CANCELLED
