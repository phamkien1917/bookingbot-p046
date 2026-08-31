"""Listing freshness — how long since a human last confirmed a listing is live.

Crawled listings die silently: the room is let, the post stays up. Freshness is
tracked apart from ``updated_at``, which any edit touches.
"""

from datetime import UTC, datetime

from src.utils.time import utcnow

# ponytail: one global threshold. Split per province or per crawl source if the
# refresh cadence turns out to differ by market.
STALE_AFTER_DAYS = 30


def verification_age(
    last_verified_at: datetime | None,
    published_at: datetime | None = None,
) -> tuple[int | None, bool]:
    """Return ``(days since last verification, is_stale)``.

    Falls back to ``published_at`` for crawled listings nobody has verified yet.
    An unknown age counts as stale: never verified is not the same as fresh.
    """
    reference = last_verified_at or published_at
    if reference is None:
        return None, True
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=UTC)
    days = max((utcnow() - reference).days, 0)
    return days, days >= STALE_AFTER_DAYS


def verification_text(days: int | None, is_stale: bool) -> str:
    """Short Vietnamese label for chat replies and cards."""
    if days is None:
        return "Chưa có mốc xác minh — Nera sẽ nhờ Sale xác nhận trước khi chốt lịch"
    if is_stale:
        return f"Xác minh {days} ngày trước — cần Sale xác nhận lại còn trống"
    if days == 0:
        return "Xác minh hôm nay"
    return f"Xác minh {days} ngày trước"
