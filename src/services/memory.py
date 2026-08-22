"""Memory service for AI agent.

Short-term memory: Redis (session state, conversation context)
Long-term memory: PostgreSQL (customer preferences, learned patterns)

This module re-exports from redis_service for backward compatibility.
"""

import json
import logging
from typing import Any, Optional
from uuid import UUID

from src.services.redis_service import (
    InMemoryFallback,
    close_redis,  # noqa: F401 - backward-compatible re-export
    get_redis,
)
from src.services.redis_service import (
    get_session_memory as _get_redis_session_memory,
)

logger = logging.getLogger(__name__)


# Re-export for backward compatibility
_in_memory_store = InMemoryFallback()


# ============== Short-term Memory (Session) ==============

class ShortTermMemory:
    """Redis-based session memory with in-process fallback.

    Now uses redis_service for Redis operations with graceful fallback.
    """

    SESSION_PREFIX = "session:"
    SESSION_TTL = 3600  # 1 hour default

    def __init__(self):
        """Initialize session memory."""
        self._redis_memory = _get_redis_session_memory()

    async def save_session(
        self,
        session_id: str,
        messages: list[dict],
        metadata: dict | None = None,
        ttl: int = SESSION_TTL,
    ) -> None:
        """Save session data to Redis.

        Args:
            session_id: Unique session identifier
            messages: List of message dicts
            metadata: Optional session metadata
            ttl: Time to live in seconds
        """
        await self._redis_memory.save_session(session_id, messages, metadata, ttl)
        logger.debug(f"Saved session {session_id} with TTL {ttl}s")

    async def get_session(self, session_id: str) -> dict | None:
        """Get session data from Redis.

        Args:
            session_id: Session identifier

        Returns:
            Session data dict or None if not found
        """
        return await self._redis_memory.get_session(session_id)

    async def append_message(
        self,
        session_id: str,
        role: str,
        content: str,
        ttl: int = SESSION_TTL,
    ) -> None:
        """Append a message to existing session.

        Args:
            session_id: Session identifier
            role: Message role (user/assistant)
            content: Message content
            ttl: Reset TTL after append
        """
        session = await self.get_session(session_id)
        messages = session["messages"] if session and "messages" in session else []
        metadata = session.get("metadata", {}) if session else {}
        messages.append({"role": role, "content": content, "timestamp": "now"})

        await self.save_session(session_id, messages, metadata=metadata, ttl=ttl)

    async def extend_session(self, session_id: str, ttl: int = SESSION_TTL) -> bool:
        """Extend session TTL.

        Args:
            session_id: Session identifier
            ttl: New TTL in seconds

        Returns:
            True if session existed and was extended
        """
        if await self._redis_memory.session_exists(session_id):
            await self._redis_memory.save_session(
                session_id,
                (await self.get_session(session_id))["messages"],
                ttl=ttl
            )
            return True
        return False

    async def delete_session(self, session_id: str) -> None:
        """Delete a session.

        Args:
            session_id: Session identifier
        """
        await self._redis_memory.delete_session(session_id)
        logger.debug(f"Deleted session {session_id}")

    async def get_all_sessions(self, customer_id: str) -> list[str]:
        """Get active session summaries for a customer."""
        return await self._redis_memory.list_sessions(customer_id)


# ============== Long-term Memory (Preferences) ==============

class LongTermMemory:
    """PostgreSQL-based long-term memory for customer preferences.

    This stores learned preferences and patterns that persist across sessions.
    """

    def __init__(self):
        """Initialize long-term memory."""
        pass

    async def save_preference(
        self,
        customer_id: str,
        key: str,
        value: Any,
        confidence: float = 1.0,
        source: str = "INFERRED",
    ) -> dict:
        """Save a customer preference.

        Args:
            customer_id: Customer UUID
            key: Preference key (e.g., "preferred_district", "budget_max")
            value: Preference value
            confidence: Confidence level (0.0-1.0)
            source: How preference was learned (EXPLICIT, INFERRED, IMPORT)

        Returns:
            Saved preference dict
        """
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference

        async with get_session_context() as session:
            import uuid

            # Check if preference exists
            from sqlalchemy import select

            from src.utils.time import utcnow
            stmt = select(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(customer_id),
                CustomerPreference.preference_key == key,
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update
                existing.preference_value = {"value": value}
                existing.confidence = confidence
                existing.source = source
                existing.last_confirmed_at = utcnow()
                pref = existing
            else:
                # Create new
                pref = CustomerPreference(
                    id=uuid.uuid4(),
                    customer_user_id=UUID(customer_id),
                    preference_key=key,
                    preference_value={"value": value},
                    confidence=confidence,
                    source=source,
                    last_confirmed_at=utcnow(),
                )
                session.add(pref)

            await session.flush()
            return {
                "id": str(pref.id),
                "key": pref.preference_key,
                "value": value,
                "confidence": pref.confidence,
                "source": pref.source,
            }

    async def get_preferences(self, customer_id: str) -> list[dict]:
        """Get all preferences for a customer.

        Args:
            customer_id: Customer UUID

        Returns:
            List of preference dicts
        """
        from sqlalchemy import select

        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference

        async with get_session_context() as session:
            stmt = select(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(customer_id),
            )
            result = await session.execute(stmt)
            prefs = result.scalars().all()

            return [
                {
                    "id": str(p.id),
                    "key": p.preference_key,
                    "value": p.preference_value.get("value") if p.preference_value else None,
                    "confidence": p.confidence,
                    "source": p.source,
                    "last_confirmed": p.last_confirmed_at.isoformat() if p.last_confirmed_at else None,
                }
                for p in prefs
            ]

    async def get_preference(
        self,
        customer_id: str,
        key: str,
    ) -> Any | None:
        """Get a specific preference.

        Args:
            customer_id: Customer UUID
            key: Preference key

        Returns:
            Preference value or None
        """
        prefs = await self.get_preferences(customer_id)
        for p in prefs:
            if p["key"] == key:
                return p["value"]
        return None

    async def get_preferred_time_slots(self, customer_id: str) -> list[str]:
        """Get customer's preferred time slots for viewing.

        Args:
            customer_id: Customer UUID

        Returns:
            List of preferred time slots (e.g., ["weekends", "after_18h"])
        """
        slots = await self.get_preference(customer_id, "preferred_time_slots")
        return slots or []

    async def learn_from_conversation(
        self,
        customer_id: str,
        conversation_summary: dict,
    ) -> None:
        """Learn preferences from conversation summary.

        Args:
            customer_id: Customer UUID
            conversation_summary: {
                "mentioned_districts": [...],
                "budget_range": {"min": X, "max": Y},
                "preferred_property_types": [...],
                "time_preferences": [...],
            }
        """
        # Learn districts
        for district in conversation_summary.get("mentioned_districts", []):
            await self.save_preference(
                customer_id,
                f"district_{district}",
                True,
                confidence=0.7,
                source="INFERRED",
            )

        # Learn budget
        budget = conversation_summary.get("budget_range", {})
        if budget.get("max"):
            await self.save_preference(
                customer_id,
                "budget_max",
                budget["max"],
                confidence=0.8,
                source="INFERRED",
            )

        # Learn property types
        for ptype in conversation_summary.get("preferred_property_types", []):
            await self.save_preference(
                customer_id,
                "property_type",
                ptype,
                confidence=0.7,
                source="INFERRED",
            )

        # Learn time preferences
        for time_slot in conversation_summary.get("time_preferences", []):
            await self.save_preference(
                customer_id,
                "preferred_time_slots",
                [time_slot],
                confidence=0.6,
                source="INFERRED",
            )

    async def delete_preference(self, customer_id: str, key: str) -> bool:
        """Delete a preference.

        Args:
            customer_id: Customer UUID
            key: Preference key

        Returns:
            True if deleted
        """
        from sqlalchemy import delete

        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference

        async with get_session_context() as session:
            stmt = delete(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(customer_id),
                CustomerPreference.preference_key == key,
            )
            result = await session.execute(stmt)
            return result.rowcount > 0


# ============== Singleton instances ==============

_short_term_memory: ShortTermMemory | None = None
_long_term_memory: LongTermMemory | None = None
_intent_cache: Optional["IntentCache"] = None


def get_short_term_memory() -> ShortTermMemory:
    """Get short-term memory singleton."""
    global _short_term_memory
    if _short_term_memory is None:
        _short_term_memory = ShortTermMemory()
    return _short_term_memory


def get_long_term_memory() -> LongTermMemory:
    """Get long-term memory singleton."""
    global _long_term_memory
    if _long_term_memory is None:
        _long_term_memory = LongTermMemory()
    return _long_term_memory


# ============== Intent Cache (short-lived) ==============

class IntentCache:
    """Cache kết quả classify_intent trong vài giây.

    Giúp tránh gọi LLM classify lặp lại khi user chat nhiều câu ngắn
    liên tiếp cùng chủ đề (vd: "Cảm ơn!", "OK", "Hiểu rồi" — nhưng những
    câu này giờ đã có fast-path smalltalk nên chủ yếu dùng cho câu dài).
    """

    PREFIX = "intent_cache:"
    TTL_SECONDS = 30

    def __init__(self):
        self._mem: dict = {}  # Fallback nếu Redis không khả dụng

    @staticmethod
    def make_key(session_id: str, message_hash: str) -> str:
        return f"{IntentCache.PREFIX}{session_id}:{message_hash}"

    @staticmethod
    def hash_messages(messages: list[dict]) -> str:
        """Hash ngắn gọn từ 5 message gần nhất để làm cache key."""
        import hashlib
        recent = messages[-5:] if messages else []
        joined = "|".join(f"{m.get('role', '?')}:{m.get('content', '')}" for m in recent)
        return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16]

    async def get(self, session_id: str, message_hash: str) -> dict | None:
        key = self.make_key(session_id, message_hash)
        # Thử Redis trước
        try:
            client = await get_redis()
            data = await client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            pass
        # Fallback in-memory
        return self._mem.get(key)

    async def set(self, session_id: str, message_hash: str, result: dict) -> None:
        key = self.make_key(session_id, message_hash)
        payload = json.dumps(result, ensure_ascii=False)
        # Thử Redis trước
        try:
            client = await get_redis()
            await client.set(key, payload, ex=self.TTL_SECONDS)
            return
        except Exception:
            pass
        # Fallback in-memory (không TTL thật, nhưng đủ cho phiên test)
        self._mem[key] = result


def get_intent_cache() -> IntentCache:
    """Get intent cache singleton."""
    global _intent_cache
    if _intent_cache is None:
        _intent_cache = IntentCache()
    return _intent_cache
