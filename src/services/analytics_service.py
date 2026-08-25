"""Small, non-blocking helpers for product funnel analytics."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AnalyticsEvent


def record_event(
    db: AsyncSession,
    event_name: str,
    *,
    customer_user_id: UUID | None = None,
    tour_request_id: UUID | None = None,
    appointment_id: UUID | None = None,
    session_id: str | None = None,
    properties: dict | None = None,
) -> None:
    """Queue an analytics event in the caller's transaction."""
    db.add(AnalyticsEvent(
        event_name=event_name,
        customer_user_id=customer_user_id,
        tour_request_id=tour_request_id,
        appointment_id=appointment_id,
        session_id=session_id,
        properties=properties or {},
    ))
