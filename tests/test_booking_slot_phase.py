"""The slot-picking phase must not swallow every message.

Waiting for a slot number is a prompt, not a cage: a customer who names another
day, or gives up, used to get "chọn từ 1 đến N" repeated until they left.
"""

import pytest

from src.agents.nodes.booking_agent import booking_agent
from src.agents.state import Intent


def slot_state(**overrides) -> dict:
    """A conversation parked on one visible slot for 01/09/2026."""
    state = {
        "intent": Intent.SELECT_SLOT,
        "phase": "AWAITING_SLOT",
        "query": "",
        "customer_id": None,
        "customer_role": None,
        "current_property_id": "11111111-1111-1111-1111-111111111111",
        "selected_slots": [
            {
                "sale_user_id": "22222222-2222-2222-2222-222222222222",
                "sale_name": "Phan Thị Xuân",
                "starts_at": "2026-09-01T16:00:00+07:00",
                "ends_at": "2026-09-01T17:00:00+07:00",
                "label": "16:00",
            }
        ],
        "selected_slot_index": None,
        "requested_date": "2026-09-01",
        "requested_hour": None,
    }
    state.update(overrides)
    return state


@pytest.mark.parametrize("intent", [Intent.DENY, Intent.GOODBYE])
async def test_giving_up_ends_the_booking_flow(intent):
    result = await booking_agent(slot_state(intent=intent, query="thôi không đặt nữa"))

    assert result["phase"] is None, "the phase must release, not loop"
    assert result["selected_slots"] == []
    assert "chọn từ 1 đến" not in result["response"]
    assert "dừng" in result["response"].lower()


async def test_unavailable_hour_is_named_instead_of_repeating_the_range():
    result = await booking_agent(slot_state(requested_hour=15, query="tôi muốn 3 giờ chiều nay"))

    assert "15:00" in result["response"], "say which hour is not free"
    assert "16:00" in result["response"], "and which one is"
    # The customer must be told there is a way out.
    assert any("ngày khác" in action.lower() for action in result["suggested_actions"])
    assert any("thôi" in action.lower() for action in result["suggested_actions"])


async def test_an_out_of_range_number_still_gets_the_slot_prompt():
    result = await booking_agent(slot_state(selected_slot_index=5, query="chọn khung 6"))

    assert "16:00" in result["response"], "list what exists rather than only the range"
    assert result.get("auth_required") is not True, "an invalid pick must not reach the auth gate"


async def test_a_valid_pick_is_not_diverted():
    """The escape hatches must not break the normal path."""
    result = await booking_agent(slot_state(selected_slot_index=0, query="1"))

    # Guest picking a slot hits the auth gate, which proves the pick was read.
    assert result.get("auth_required") is True
    assert result.get("selected_slot_index") == 0


@pytest.mark.parametrize(
    "message",
    [
        "tôi không muốn đặt nữa không có thời gian ưng ý",
        "thôi không đặt nữa",
        "để hôm khác đi",
        "bỏ qua",
    ],
)
async def test_giving_up_in_a_full_sentence_still_exits(message):
    """The classifier labels short refusals; a whole sentence must work too."""
    result = await booking_agent(slot_state(intent=Intent.BOOK_APPOINTMENT, query=message))

    assert result["phase"] is None, f"{message!r} left the customer stuck"
    assert "chọn từ 1 đến" not in result["response"]


@pytest.mark.parametrize(
    "message",
    [
        "căn này không có ban công à",
        "còn căn nào rẻ hơn nữa không",
        "chọn khung 1",
    ],
)
async def test_ordinary_questions_are_not_read_as_giving_up(message):
    result = await booking_agent(slot_state(intent=Intent.SELECT_SLOT, query=message))

    assert result.get("phase") is not None or result.get("auth_required") or result.get("response")
    assert "Mình đã dừng việc đặt lịch" not in result["response"]


async def test_a_different_hour_is_confirmed_not_booked():
    """Asking for 15:00 must never silently book the 16:00 slot."""
    state = slot_state(
        intent=Intent.SELECT_SLOT,
        query="tôi muốn 3 giờ chiều nay",
        selected_slot_index=0,
    )
    state["selected_slots"][0]["sale_name"] = "Phan Thị Xuân"

    result = await booking_agent(state)

    assert result.get("auth_required") is not True, "must not proceed to booking"
    assert result["selected_slot_index"] is None, "the pick is withdrawn until confirmed"
    assert "15:00" in result["response"] and "16:00" in result["response"]


async def test_picking_the_matching_hour_goes_straight_through():
    state = slot_state(intent=Intent.SELECT_SLOT, query="lấy khung 16:00", selected_slot_index=0)

    result = await booking_agent(state)

    assert result.get("auth_required") is True, "same hour must not be second-guessed"


async def test_a_bare_ordinal_is_not_second_guessed():
    """"chọn khung 1" names no hour, so there is nothing to disagree with."""
    state = slot_state(intent=Intent.SELECT_SLOT, query="chọn khung giờ 1", selected_slot_index=0)

    result = await booking_agent(state)

    assert result.get("auth_required") is True
