from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

from src.utils.freshness import STALE_AFTER_DAYS, verification_age, verification_text


def _days_ago(days: int) -> datetime:
    return datetime.now(UTC) - timedelta(days=days, hours=1)


def test_recent_verification_is_fresh():
    days, stale = verification_age(_days_ago(3))
    assert days == 3
    assert stale is False


def test_verification_older_than_threshold_is_stale():
    days, stale = verification_age(_days_ago(STALE_AFTER_DAYS + 5))
    assert days == STALE_AFTER_DAYS + 5
    assert stale is True


def test_threshold_day_itself_counts_as_stale():
    _, stale = verification_age(_days_ago(STALE_AFTER_DAYS))
    assert stale is True


def test_falls_back_to_published_at_when_never_verified():
    days, stale = verification_age(None, _days_ago(400))
    assert days == 400
    assert stale is True


def test_last_verified_at_wins_over_published_at():
    days, stale = verification_age(_days_ago(2), _days_ago(400))
    assert days == 2
    assert stale is False


def test_unknown_age_counts_as_stale():
    assert verification_age(None, None) == (None, True)


def test_naive_datetime_does_not_crash():
    naive = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=10)
    days, stale = verification_age(naive)
    assert days == 10
    assert stale is False


def test_future_timestamp_clamps_to_zero():
    days, stale = verification_age(datetime.now(UTC) + timedelta(days=3))
    assert days == 0
    assert stale is False


def test_labels_say_what_the_sale_must_do():
    assert "xác nhận lại" in verification_text(45, True)
    assert verification_text(0, False) == "Xác minh hôm nay"
    assert "Chưa có mốc xác minh" in verification_text(None, True)


def test_serialized_property_carries_freshness_to_cards_and_prompt():
    from src.agents.nodes.inventory_agent import serialize_property_item

    prop = SimpleNamespace(
        id=uuid4(),
        code="NT-1",
        property_kind=None,
        title="Căn hộ test",
        description=None,
        status=None,
        address_line=None,
        ward=None,
        district="Cầu Giấy",
        province="Hà Nội",
        latitude=None,
        longitude=None,
        area_sqm=40,
        bedrooms=1,
        bathrooms=1,
        floor_number=None,
        orientation=None,
        legal_status=None,
        list_price=3_000_000_000,
        currency="VND",
        features={},
        media=[],
        published_at=_days_ago(400),
        last_verified_at=_days_ago(2),
    )
    item = serialize_property_item(prop)

    # last_verified_at wins over a long-published listing.
    assert item["verified_days_ago"] == 2
    assert item["is_stale"] is False
    assert item["verification_label"] == "Xác minh 2 ngày trước"
    assert item["last_verified_at"] is not None
