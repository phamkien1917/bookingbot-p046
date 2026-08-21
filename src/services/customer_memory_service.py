"""Long-term customer memory stored in PostgreSQL."""

from __future__ import annotations

import re
from src.utils.time import utcnow
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CustomerPreference

SEARCH_MEMORY_KEYS = {
    "district", "province", "property_kind", "min_price", "max_price",
    "min_bedrooms", "min_bathrooms", "min_area",
}


def _as_uuid(value: str) -> UUID | None:
    try:
        return UUID(value)
    except (TypeError, ValueError):
        return None


def _unwrap(value: dict) -> object:
    return value.get("value") if set(value).issubset({"value"}) else value


async def get_customer_memory(db: AsyncSession, customer_id: str) -> dict:
    """Return the latest normalized preference map for one customer."""
    customer_uuid = _as_uuid(customer_id)
    if not customer_uuid:
        return {}
    rows = (await db.execute(
        select(CustomerPreference)
        .where(CustomerPreference.customer_user_id == customer_uuid)
        .order_by(CustomerPreference.updated_at.desc())
    )).scalars().all()
    return {row.preference_key: _unwrap(row.preference_value) for row in rows}


async def _upsert(
    db: AsyncSession,
    customer_id: str,
    key: str,
    value: object,
    *,
    confidence: float = 0.9,
    source: str = "INFERRED",
) -> None:
    customer_uuid = _as_uuid(customer_id)
    if not customer_uuid:
        return
    row = await db.scalar(select(CustomerPreference).where(
        CustomerPreference.customer_user_id == customer_uuid,
        CustomerPreference.preference_key == key,
    ))
    payload = {"value": value}
    if row:
        row.preference_value = payload
        row.confidence = confidence
        row.source = source
        row.last_confirmed_at = utcnow()
    else:
        db.add(CustomerPreference(
            customer_user_id=customer_uuid,
            preference_key=key,
            preference_value=payload,
            confidence=confidence,
            source=source,
            last_confirmed_at=utcnow(),
        ))


async def remember_search_criteria(
    db: AsyncSession,
    customer_id: str,
    criteria: dict | None,
) -> None:
    """Synchronize durable preferences with the active search criteria."""
    if not criteria:
        return
    for key in SEARCH_MEMORY_KEYS:
        value = criteria.get(key)
        if value is None or value == "":
            await forget_customer_memory(db, customer_id, key)
            continue
        await _upsert(db, customer_id, key, value, confidence=0.92)


async def remember_feedback(db: AsyncSession, customer_id: str, message: str) -> bool:
    """Keep explicit preference/feedback sentences as a short rolling memory."""
    normalized = message.strip()
    if not re.search(
        r"\b(tôi|mình|em)\s+(thích|ưu tiên|muốn|không thích|không hợp|không muốn|cần)\b",
        normalized,
        flags=re.IGNORECASE,
    ):
        return False
    memory = await get_customer_memory(db, customer_id)
    notes = memory.get("feedback_notes", [])
    if not isinstance(notes, list):
        notes = []
    notes = [item for item in notes if item != normalized][-7:] + [normalized[:500]]
    await _upsert(db, customer_id, "feedback_notes", notes, confidence=1.0, source="EXPLICIT")
    return True


async def forget_customer_memory(db: AsyncSession, customer_id: str, key: str | None = None) -> int:
    customer_uuid = _as_uuid(customer_id)
    if not customer_uuid:
        return 0
    statement = delete(CustomerPreference).where(CustomerPreference.customer_user_id == customer_uuid)
    if key:
        statement = statement.where(CustomerPreference.preference_key == key)
    result = await db.execute(statement)
    return result.rowcount or 0


def memory_summary(memory: dict) -> str:
    """Build a short, user-facing Vietnamese summary without exposing internals."""
    parts: list[str] = []
    location = memory.get("district") or memory.get("province")
    if location:
        parts.append(str(location))
    minimum, maximum = memory.get("min_price"), memory.get("max_price")
    if isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)):
        parts.append(f"{minimum / 1e9:g}–{maximum / 1e9:g} tỷ")
    elif isinstance(maximum, (int, float)):
        parts.append(f"dưới {maximum / 1e9:g} tỷ")
    elif isinstance(minimum, (int, float)):
        parts.append(f"từ {minimum / 1e9:g} tỷ")
    bedrooms = memory.get("min_bedrooms")
    if bedrooms:
        parts.append(f"{bedrooms} phòng ngủ+")
    if memory.get("min_area"):
        parts.append(f"từ {memory['min_area']:g} m²")
    notes = memory.get("feedback_notes")
    if isinstance(notes, list) and notes:
        parts.append(notes[-1])
    return " · ".join(parts)
