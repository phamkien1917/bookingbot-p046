"""Two customers racing for the same property must not both get a hold.

Double-booking is the failure this product is built to prevent, and it is the
centrepiece of the demo, yet nothing pinned the mechanism down. The existing two
hold tests walk the happy path and the already-held path sequentially, which
cannot tell a real race apart from a lucky ordering.

Proving a genuine two-transaction race needs a live PostgreSQL, which CI does not
have. So this file locks down the two things that make the race safe and that a
refactor could silently remove:

  1. the advisory lock is taken BEFORE the availability read
  2. the unique partial index exists as the second line of defence

Both are deterministic and run everywhere. The end-to-end race stays a manual
check against a real database; see the bottom of this file.
"""

import inspect
import re
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.database.migrations import POSTGRES_MIGRATIONS
from src.exceptions import BookingConflictError
from src.services.property_hold_service import create_hold_for_appointment

SOURCE = inspect.getsource(create_hold_for_appointment)


def test_the_advisory_lock_is_taken_before_the_availability_read():
    """Reading first and locking after leaves the whole race window open."""
    lock_at = SOURCE.find("pg_advisory_xact_lock")
    read_at = SOURCE.find("PropertyHold.property_id ==")

    assert lock_at != -1, "the advisory lock is what serialises two racing transactions"
    assert read_at != -1, "the availability read moved; this test needs updating"
    assert lock_at < read_at, "locking after the read means both callers can see a free slot"


def test_the_lock_key_is_per_property_not_global():
    """A global lock would serialise every booking in the system."""
    key = re.search(r'"key": f"([^"]+)"', SOURCE)

    assert key, "the advisory lock needs a key derived from the property"
    assert "appointment.property_id" in key.group(1)


def test_a_unique_index_backs_the_lock_up():
    """If the lock is ever bypassed, PostgreSQL still refuses the second row."""
    migration_sql = "\n".join(POSTGRES_MIGRATIONS)

    assert "uq_property_holds_one_active_property" in migration_sql
    assert "ON property_holds(property_id) WHERE status = 'ACTIVE'" in migration_sql, (
        "a partial index on ACTIVE is what allows repeated expired holds "
        "while still permitting only one live one"
    )


async def test_the_second_caller_is_refused_while_a_hold_is_live():
    """The read the lock protects has to actually reject, not warn."""
    from datetime import timedelta
    from types import SimpleNamespace
    from uuid import uuid4

    from src.database.models import HoldStatus
    from src.utils.time import utcnow

    appointment = SimpleNamespace(
        id=uuid4(), property_id=uuid4(), customer_user_id=uuid4(), sale_user_id=uuid4()
    )
    live_hold = SimpleNamespace(
        status=HoldStatus.ACTIVE, expires_at=utcnow() + timedelta(minutes=10)
    )
    db = MagicMock()
    db.execute = AsyncMock()
    db.scalar = AsyncMock(side_effect=[None, live_hold])
    db.flush = AsyncMock()

    with pytest.raises(BookingConflictError):
        await create_hold_for_appointment(db, appointment, appointment.sale_user_id)

    db.add.assert_not_called()


async def test_an_expired_hold_does_not_block_the_next_customer():
    """15 minutes is a hold, not a reservation. Expiry has to free the slot."""
    from datetime import timedelta
    from types import SimpleNamespace
    from uuid import uuid4

    from src.database.models import HoldStatus
    from src.utils.time import utcnow

    appointment = SimpleNamespace(
        id=uuid4(), property_id=uuid4(), customer_user_id=uuid4(), sale_user_id=uuid4()
    )
    stale = SimpleNamespace(
        status=HoldStatus.ACTIVE,
        expires_at=utcnow() - timedelta(minutes=1),
        released_at=None,
        release_reason=None,
    )
    db = MagicMock()
    db.execute = AsyncMock()
    db.scalar = AsyncMock(side_effect=[None, stale])
    db.flush = AsyncMock()

    hold = await create_hold_for_appointment(db, appointment, appointment.sale_user_id)

    assert stale.status == HoldStatus.EXPIRED, "the stale hold has to be retired, not ignored"
    assert stale.release_reason == "AUTO_EXPIRED_ON_CREATE"
    assert hold.status == HoldStatus.ACTIVE
    db.add.assert_called_once_with(hold)


def test_the_default_hold_window_comes_from_settings_not_a_literal():
    """The 15 minutes is a product rule; it must stay configurable in one place."""
    assert "get_settings().hold_default_minutes" in SOURCE
    assert "hold_minutes must be positive" in SOURCE


# ── Manual check, needs a real PostgreSQL ────────────────────────────────────
#
# The assertions above prove the mechanism is wired correctly. Proving that two
# concurrent transactions actually serialise needs a live database, because the
# guarantee comes from PostgreSQL, not from this code:
#
#   docker compose up -d db
#   python - <<'PY'
#   import asyncio
#   from src.database.connection import get_session_context
#   from src.services.property_hold_service import create_hold_for_appointment
#
#   async def racer(appointment, sale_id):
#       async with get_session_context() as session:
#           return await create_hold_for_appointment(session, appointment, sale_id)
#
#   # two appointments on the SAME property_id, fired together
#   results = asyncio.run(asyncio.gather(
#       racer(a1, sale), racer(a2, sale), return_exceptions=True
#   ))
#   # expected: exactly one PropertyHold, one BookingConflictError
#   PY
