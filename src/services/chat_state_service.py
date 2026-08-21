"""Deterministic, JSON-serializable state helpers for production chat.

The LangGraph package is owned by another team member.  The public chat API keeps
its durable workflow state here so a request can recover after Redis loss, login,
or a backend restart without depending on in-memory graph state.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
STATE_VERSION = 1


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower().strip())
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", normalized.replace("đ", "d"))


def default_chat_state() -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "phase": "IDLE",
        "criteria": {},
        "soft_preferences": [],
        "household_context": [],
        "commute_landmark": None,
        "max_commute_minutes": None,
        "property_refs": [],
        "selected_property_id": None,
        "selected_property_index": None,
        "requested_date": None,
        "requested_hour": None,
        "slots": [],
        "selected_slot_index": None,
        "active_request_id": None,
        "active_request_code": None,
        "pending_action": None,
    }


def load_chat_state(metadata: dict | None) -> dict[str, Any]:
    state = default_chat_state()
    stored = (metadata or {}).get("chat_state")
    if isinstance(stored, dict) and stored.get("version") == STATE_VERSION:
        for key in state:
            if key in stored:
                state[key] = stored[key]
    return state


def save_chat_state(metadata: dict | None, state: dict[str, Any]) -> dict:
    result = dict(metadata or {})
    result["chat_state"] = {key: state.get(key) for key in default_chat_state()}
    return result


def extract_ordinal(message: str, *, maximum: int | None = None) -> int | None:
    """Return a zero-based ordinal used for property or slot references."""
    text = normalize_text(message)
    word_ordinals = {
        "dau tien": 0,
        "thu nhat": 0,
        "mot": 0,
        "thu hai": 1,
        "hai": 1,
        "thu ba": 2,
        "ba": 2,
        "thu tu": 3,
        "bon": 3,
        "thu nam": 4,
        "nam": 4,
        "cuoi": (maximum - 1) if maximum else -1,
    }
    numeric = re.search(
        r"(?:can|nha|bat dong san|lua chon|phuong an|slot|khung gio|gio|so)\s*"
        r"(?:so|thu)?\s*#?\s*(\d{1,2})\b",
        text,
    )
    if numeric:
        index = int(numeric.group(1)) - 1
    elif re.fullmatch(r"\s*[1-9]\s*", text):
        index = int(text) - 1
    else:
        index = next(
            (value for token, value in word_ordinals.items() if re.search(rf"\b{token}\b", text)),
            None,
        )
    if index is None or index < 0:
        return None
    if maximum is not None and index >= maximum:
        return None
    return index


def parse_requested_date(message: str, *, now: datetime | None = None) -> date | None:
    text = normalize_text(message)
    current = (now or datetime.now(LOCAL_TZ)).astimezone(LOCAL_TZ)

    iso_match = re.search(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b", text)
    if iso_match:
        try:
            return date(*(int(value) for value in iso_match.groups()))
        except ValueError:
            return None

    vietnamese_match = re.search(r"\b(?:ngay\s*)?(\d{1,2})[/-](\d{1,2})(?:[/-](20\d{2}))?\b", text)
    if vietnamese_match:
        day, month, year = vietnamese_match.groups()
        try:
            candidate = date(int(year or current.year), int(month), int(day))
            if not year and candidate < current.date():
                candidate = candidate.replace(year=candidate.year + 1)
            return candidate
        except ValueError:
            return None

    if re.search(r"\b(ngay kia|mot kia)\b", text):
        return current.date() + timedelta(days=2)
    if re.search(r"\b(ngay mai|mai)\b", text):
        return current.date() + timedelta(days=1)
    if re.search(r"\bhom nay\b", text):
        return current.date()

    weekdays = {
        "thu hai": 0,
        "thu ba": 1,
        "thu tu": 2,
        "thu nam": 3,
        "thu sau": 4,
        "thu bay": 5,
        "chu nhat": 6,
    }
    for token, weekday in weekdays.items():
        if re.search(rf"\b{token}\b", text):
            days = (weekday - current.weekday()) % 7
            if days == 0 and "tuan sau" in text:
                days = 7
            elif "tuan sau" in text:
                days += 7
            return current.date() + timedelta(days=days)
    return None


def parse_requested_hour(message: str) -> int | None:
    text = normalize_text(message)
    match = re.search(r"\b([01]?\d|2[0-3])\s*(?:h|gio)(?:\s*(\d{1,2}))?\b", text)
    if match:
        hour = int(match.group(1))
        if "chieu" in text and 1 <= hour < 12:
            hour += 12
        return hour
    if "buoi sang" in text or re.search(r"\bsang\b", text):
        return 9
    if "buoi chieu" in text or re.search(r"\bchieu\b", text):
        return 14
    return None


def is_affirmative(message: str) -> bool:
    return normalize_text(message) in {
        "co", "dong y", "xac nhan", "tiep tuc", "dat di", "ok", "okay", "dung", "dung roi"
    }


def is_negative(message: str) -> bool:
    return normalize_text(message) in {"khong", "khong can", "thoi", "bo qua", "huy thao tac"}
