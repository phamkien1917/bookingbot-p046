"""A request waiting on a sale must never be reported as a confirmed appointment.

The product rule is that Nera orchestrates but a human decides: a tour_request
only becomes an appointment after the sale accepts. The wording the customer
reads is the only place that rule is visible to them, so it is worth pinning.
Nothing in the suite checked it before.
"""

import inspect
import re

import pytest

from src.agents.nodes.booking_agent import booking_agent
from src.agents.state import Intent
from src.database.models import RequestStatus

# What "the sale already said yes" sounds like in Vietnamese. A reply carrying any
# of these while the request is still WAITING_APPROVAL is a false confirmation.
CONFIRMED_PHRASES = (
    "đã được xác nhận",
    "đã xác nhận lịch",
    "sale đã duyệt",
    "đã duyệt lịch",
    "lịch hẹn đã hoàn tất",
)


def says_confirmed(text: str) -> list[str]:
    lowered = (text or "").lower()
    return [phrase for phrase in CONFIRMED_PHRASES if phrase in lowered]


BODY = inspect.getsource(booking_agent)


def test_waiting_approval_is_the_status_the_customer_is_shown():
    """The success message must name the real state, not imply a decision."""
    body = BODY

    # The block that reports a created request.
    assert "Đã {verb} thành công" in body
    assert "WAITING_APPROVAL" in body
    assert "Đang chờ Sale xác nhận" in body, "the customer has to see that a human still has to act"


def test_no_branch_tells_the_customer_the_booking_is_confirmed():
    """Scan every literal the booking node can emit."""
    body = BODY

    # Strings the node builds for the customer, minus comments.
    literals = re.findall(r'"([^"\\]{12,})"', body)
    offenders = [text for text in literals if says_confirmed(text)]

    assert not offenders, f"booking node can claim a confirmation it does not have: {offenders}"


def test_the_verb_used_never_asserts_approval():
    """`verb` is interpolated into 'Đã {verb} thành công'."""
    verbs = re.findall(r'verb = "([^"]+)"', BODY)

    assert verbs, "the message template still has to be built from a verb"
    for verb in verbs:
        assert not says_confirmed(f"đã {verb}"), f"verb {verb!r} reads as an approval"
        assert "xác nhận" not in verb, f"verb {verb!r} claims the sale acted"


@pytest.mark.parametrize(
    "status",
    [RequestStatus.WAITING_APPROVAL, RequestStatus.DRAFT],
)
def test_pending_statuses_are_not_the_booked_state(status):
    """Guards the enum itself: a pending request is not a confirmed one."""
    assert status != RequestStatus.BOOKED


async def test_slot_phase_reply_does_not_promise_a_confirmation():
    """The customer picking a slot is not the sale approving it."""
    state = {
        "intent": Intent.SELECT_SLOT,
        "phase": "AWAITING_SLOT",
        "query": "chọn khung 1",
        "customer_id": None,
        "customer_role": None,
        "current_property_id": "11111111-1111-1111-1111-111111111111",
        "selected_slots": [
            {
                "sale_user_id": "22222222-2222-2222-2222-222222222222",
                "sale_name": "Phan Thị Xuân",
                "starts_at": "2026-09-02T16:00:00+07:00",
                "ends_at": "2026-09-02T17:00:00+07:00",
                "label": "16:00",
            }
        ],
        "selected_slot_index": 0,
        "requested_date": "2026-09-02",
        "requested_hour": None,
    }

    result = await booking_agent(state)

    assert not says_confirmed(result["response"]), result["response"]
