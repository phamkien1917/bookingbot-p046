"""Long-term customer memory stored in PostgreSQL."""

from __future__ import annotations

import re
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CustomerPreference
from src.services.chat_state_service import normalize_text
from src.utils.time import utcnow

SEARCH_MEMORY_KEYS = {
    "region", "district", "province", "property_kind", "min_price", "max_price",
    "min_bedrooms", "max_bedrooms", "min_bathrooms", "min_area",
    "transaction_type", "orientation", "legal_status", "furniture_status",
    "min_floor", "max_floor",
}

TIME_PREFERENCE_KEY = "preferred_time_slots"


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


def extract_time_preferences(message: str) -> list[str]:
    """Extract stable viewing-time preferences, not one-off appointment dates."""
    text = normalize_text(message)
    preferences: list[str] = []
    patterns = (
        (r"\b(buoi sang|sang som|truoc 12h)\b", "MORNING"),
        (r"\b(buoi chieu|chieu toi|tu 13h|sau 13h)\b", "AFTERNOON"),
        (r"\b(buoi toi|sau 18h|ngoai gio|tan lam)\b", "AFTER_18"),
        (r"\b(cuoi tuan|thu bay|chu nhat)\b", "WEEKEND"),
        (r"\b(ngay thuong|thu 2|thu hai|thu 3|thu ba|thu 4|thu tu|thu 5|thu nam|thu 6|thu sau)\b", "WEEKDAY"),
    )
    for pattern, value in patterns:
        if re.search(pattern, text):
            preferences.append(value)
    return preferences


async def remember_time_preferences(
    db: AsyncSession,
    customer_id: str,
    message: str,
) -> bool:
    """Persist explicit recurring time preferences from a customer message."""
    if not re.search(r"\b(thich|uu tien|thuong|tien|phu hop|chi co the|muon)\b", normalize_text(message)):
        return False
    extracted = extract_time_preferences(message)
    if not extracted:
        return False
    memory = await get_customer_memory(db, customer_id)
    current = memory.get(TIME_PREFERENCE_KEY, [])
    if not isinstance(current, list):
        current = []
    merged = list(dict.fromkeys([*current, *extracted]))[-6:]
    await _upsert(db, customer_id, TIME_PREFERENCE_KEY, merged, confidence=0.95, source="EXPLICIT")
    return True


async def remember_selected_booking_time(
    db: AsyncSession,
    customer_id: str,
    starts_at: datetime,
) -> None:
    """Learn a low-confidence preference after repeated/actual booking behavior."""
    labels = ["WEEKEND" if starts_at.weekday() >= 5 else "WEEKDAY"]
    if starts_at.hour < 12:
        labels.append("MORNING")
    elif starts_at.hour < 18:
        labels.append("AFTERNOON")
    else:
        labels.append("AFTER_18")
    memory = await get_customer_memory(db, customer_id)
    current = memory.get(TIME_PREFERENCE_KEY, [])
    if not isinstance(current, list):
        current = []
    await _upsert(
        db,
        customer_id,
        TIME_PREFERENCE_KEY,
        list(dict.fromkeys([*current, *labels]))[-6:],
        confidence=0.7,
        source="BEHAVIORAL",
    )


async def get_preferred_time_slots(db: AsyncSession, customer_id: str) -> list[str]:
    memory = await get_customer_memory(db, customer_id)
    value = memory.get(TIME_PREFERENCE_KEY, [])
    return value if isinstance(value, list) else []


def time_preference_score(starts_at: datetime, preferences: list[str]) -> int:
    score = 0
    if starts_at.weekday() >= 5 and "WEEKEND" in preferences:
        score += 2
    if starts_at.weekday() < 5 and "WEEKDAY" in preferences:
        score += 1
    if starts_at.hour < 12 and "MORNING" in preferences:
        score += 2
    elif 12 <= starts_at.hour < 18 and "AFTERNOON" in preferences:
        score += 2
    elif starts_at.hour >= 18 and "AFTER_18" in preferences:
        score += 2
    return score




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
    is_rental = memory.get("transaction_type") == "RENT"
    unit = 1e6 if is_rental else 1e9
    unit_label = "triệu/tháng" if is_rental else "tỷ"
    if isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)):
        parts.append(f"{minimum / unit:g}–{maximum / unit:g} {unit_label}")
    elif isinstance(maximum, (int, float)):
        parts.append(f"dưới {maximum / unit:g} {unit_label}")
    elif isinstance(minimum, (int, float)):
        parts.append(f"từ {minimum / unit:g} {unit_label}")
    bedrooms = memory.get("min_bedrooms")
    if bedrooms:
        parts.append(f"{bedrooms} phòng ngủ+")
    if memory.get("min_area"):
        try:
            parts.append(f"từ {float(memory['min_area']):g} m²")
        except (ValueError, TypeError):
            parts.append(f"từ {memory['min_area']} m²")
    if memory.get("orientation"):
        parts.append(f"hướng {memory['orientation']}")
    if memory.get("legal_status"):
        parts.append(str(memory["legal_status"]))
    notes = memory.get("feedback_notes")
    if isinstance(notes, list) and notes:
        last_note = str(notes[-1]).strip()
        if not any(kw in last_note.lower() for kw in ["thay đổi nhu cầu", "tiếp tục", "tìm kiếm"]):
            parts.append(last_note)
    time_labels = memory.get(TIME_PREFERENCE_KEY)
    if isinstance(time_labels, list) and time_labels:
        readable = {
            "MORNING": "ưu tiên buổi sáng",
            "AFTERNOON": "ưu tiên buổi chiều",
            "AFTER_18": "ưu tiên sau 18h",
            "WEEKEND": "ưu tiên cuối tuần",
            "WEEKDAY": "ưu tiên ngày thường",
        }
        parts.extend(readable[item] for item in time_labels if item in readable)
    return " · ".join(parts)
