"""One-time OAuth login code exchange backed by Redis."""

import json
import secrets

from src.services.redis_service import get_redis

CODE_TTL_SECONDS = 60
KEY_PREFIX = "oauth_login_exchange:"


async def create_oauth_exchange(user_id: str, role: str) -> str:
    """Persist a short-lived opaque code; OAuth fails closed without Redis."""
    code = secrets.token_urlsafe(32)
    client = await get_redis()
    await client.set(
        f"{KEY_PREFIX}{code}",
        json.dumps({"user_id": user_id, "role": role}),
        ex=CODE_TTL_SECONDS,
        nx=True,
    )
    return code


async def consume_oauth_exchange(code: str) -> dict[str, str] | None:
    """Atomically read and delete an exchange code using Redis 5-compatible Lua."""
    client = await get_redis()
    raw = await client.eval(
        "local v=redis.call('GET',KEYS[1]); "
        "if v then redis.call('DEL',KEYS[1]) end; return v",
        1,
        f"{KEY_PREFIX}{code}",
    )
    if not raw:
        return None
    payload = json.loads(raw)
    if not payload.get("user_id") or not payload.get("role"):
        return None
    return {"user_id": str(payload["user_id"]), "role": str(payload["role"])}
