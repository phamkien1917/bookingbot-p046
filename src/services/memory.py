"""Memory service for AI agent.

Short-term memory: Redis (session state, conversation context)
Long-term memory: PostgreSQL (customer preferences, learned patterns)
"""

import json
import logging
from typing import Any, Optional
from uuid import UUID

import redis.asyncio as redis

from src.config import get_settings

logger = logging.getLogger(__name__)


# ============== Redis Connection ==============

_redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None


# ============== Short-term Memory (Session) ==============

class ShortTermMemory:
    """Redis-based session memory for conversation context."""

    SESSION_PREFIX = "session:"
    SESSION_TTL = 3600  # 1 hour default

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        """Initialize with Redis client."""
        self._redis = redis_client

    async def _get_client(self) -> redis.Redis:
        """Get Redis client."""
        if self._redis is None:
            self._redis = await get_redis()
        return self._redis

    def _session_key(self, session_id: str) -> str:
        """Get Redis key for session."""
        return f"{self.SESSION_PREFIX}{session_id}"

    async def save_session(
        self,
        session_id: str,
        messages: list[dict],
        metadata: Optional[dict] = None,
        ttl: int = SESSION_TTL,
    ) -> None:
        """Save session data to Redis.

        Args:
            session_id: Unique session identifier
            messages: List of message dicts
            metadata: Optional session metadata
            ttl: Time to live in seconds
        """
        client = await self._get_client()
        key = self._session_key(session_id)

        data = {
            "messages": json.dumps(messages),
            "metadata": json.dumps(metadata or {}),
        }

        await client.hset(key, mapping=data)
        await client.expire(key, ttl)

        logger.debug(f"Saved session {session_id} with TTL {ttl}s")

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data from Redis.

        Args:
            session_id: Session identifier

        Returns:
            Session data dict or None if not found
        """
        client = await self._get_client()
        key = self._session_key(session_id)

        data = await client.hgetall(key)
        if not data:
            return None

        return {
            "messages": json.loads(data.get("messages", "[]")),
            "metadata": json.loads(data.get("metadata", "{}")),
        }

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
        messages = session["messages"] if session else []
        messages.append({"role": role, "content": content, "timestamp": "now"})

        await self.save_session(session_id, messages, ttl=ttl)

    async def extend_session(self, session_id: str, ttl: int = SESSION_TTL) -> bool:
        """Extend session TTL.

        Args:
            session_id: Session identifier
            ttl: New TTL in seconds

        Returns:
            True if session existed and was extended
        """
        client = await self._get_client()
        key = self._session_key(session_id)

        if await client.exists(key):
            await client.expire(key, ttl)
            return True
        return False

    async def delete_session(self, session_id: str) -> None:
        """Delete a session.

        Args:
            session_id: Session identifier
        """
        client = await self._get_client()
        key = self._session_key(session_id)
        await client.delete(key)
        logger.debug(f"Deleted session {session_id}")

    async def get_all_sessions(self, customer_id: str) -> list[str]:
        """Get all active session IDs for a customer.

        Args:
            customer_id: Customer UUID

        Returns:
            List of session IDs
        """
        client = await self._get_client()
        pattern = f"{self.SESSION_PREFIX}*"
        keys = []

        async for key in client.scan_iter(match=pattern):
            # Check if this session belongs to customer
            data = await client.hget(key, "metadata")
            if data:
                metadata = json.loads(data)
                if metadata.get("customer_id") == customer_id:
                    keys.append(key.replace(self.SESSION_PREFIX, ""))

        return keys


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
            from datetime import datetime, timedelta

            # Check if preference exists
            from sqlalchemy import select
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
                existing.last_confirmed_at = datetime.utcnow()
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
                    last_confirmed_at=datetime.utcnow(),
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
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference
        from sqlalchemy import select

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
    ) -> Optional[Any]:
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
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference
        from sqlalchemy import delete

        async with get_session_context() as session:
            stmt = delete(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(customer_id),
                CustomerPreference.preference_key == key,
            )
            result = await session.execute(stmt)
            return result.rowcount > 0


# ============== Singleton instances ==============

_short_term_memory: Optional[ShortTermMemory] = None
_long_term_memory: Optional[LongTermMemory] = None


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
