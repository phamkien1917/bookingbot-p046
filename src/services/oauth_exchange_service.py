"""One-time OAuth login code exchange backed by Redis with in-memory fallback."""

import json
import logging
import secrets
import time

from src.services.redis_service import get_redis

logger = logging.getLogger(__name__)

CODE_TTL_SECONDS = 120
KEY_PREFIX = "oauth_login_exchange:"

# In-memory store fallback when Redis is not available: {code: (payload, expire_at)}
_in_memory_exchange_store: dict[str, tuple[dict[str, str], float]] = {}


def _cleanup_expired_in_memory() -> None:
    now = time.time()
    expired = [k for k, (_, exp) in _in_memory_exchange_store.items() if exp < now]
    for k in expired:
        _in_memory_exchange_store.pop(k, None)


async def create_oauth_exchange(user_id: str, role: str) -> str:
    """Persist a short-lived opaque code; uses Redis with in-memory fallback."""
    code = secrets.token_urlsafe(32)
    payload = {"user_id": user_id, "role": role}

    try:
        client = await get_redis()
        if client:
            await client.set(
                f"{KEY_PREFIX}{code}",
                json.dumps(payload),
                ex=CODE_TTL_SECONDS,
                nx=True,
            )
            return code
    except Exception as exc:
        logger.warning("Redis unavailable for OAuth exchange (%s), using in-memory store", exc)

    # In-memory fallback
    _cleanup_expired_in_memory()
    _in_memory_exchange_store[code] = (payload, time.time() + CODE_TTL_SECONDS)
    return code


async def consume_oauth_exchange(code: str) -> dict[str, str] | None:
    """Atomically read and delete an exchange code using Redis or in-memory fallback."""
    try:
        client = await get_redis()
        if client:
            raw = await client.eval(
                "local v=redis.call('GET',KEYS[1]); "
                "if v then redis.call('DEL',KEYS[1]) end; return v",
                1,
                f"{KEY_PREFIX}{code}",
            )
            if raw:
                payload = json.loads(raw)
                if payload.get("user_id") and payload.get("role"):
                    return {"user_id": str(payload["user_id"]), "role": str(payload["role"])}
    except Exception as exc:
        logger.warning("Redis unavailable for OAuth exchange consume (%s), checking in-memory store", exc)

    # In-memory fallback
    _cleanup_expired_in_memory()
    item = _in_memory_exchange_store.pop(code, None)
    if not item:
        return None
    payload, expire_at = item
    if time.time() > expire_at:
        return None
    if not payload.get("user_id") or not payload.get("role"):
        return None
    return {"user_id": str(payload["user_id"]), "role": str(payload["role"])}
