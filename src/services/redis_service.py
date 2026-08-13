"""Redis Service Module for BookingBot Agent.

Provides:
1. Distributed Lock - Prevent duplicate processing
2. Rate Limiting - Request throttling
3. Property Cache - Cache property queries
4. Session Memory - Redis-backed session storage
5. Message Queue - Async job queue
6. Pub/Sub - Real-time event system
7. Property Hold Manager - Temporary property holds

Redis version compatibility: Works with Redis 5.x+ (uses protocol=2 for old servers)
"""

import asyncio
import hashlib
import json
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as redis

from src.config import get_settings

logger = logging.getLogger(__name__)

# ============== Redis Connection ==============

_redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    """Get or create Redis client.

    Uses protocol=2 for compatibility with Redis 5.x servers
    that don't support RESP3 (HELLO command).
    """
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        try:
            _redis_client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                protocol=2,  # RESP2 for old Redis compatibility
                socket_connect_timeout=0.5,
                socket_timeout=0.75,
                retry_on_timeout=False,
            )
            # Test connection
            await _redis_client.ping()
            logger.info(f"Redis connected: {settings.redis_url}")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}), using fallback mode")
            _redis_client = None
            raise
    return _redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")


async def is_redis_available() -> bool:
    """Check if Redis is available."""
    try:
        client = await get_redis()
        await client.ping()
        return True
    except Exception:
        return False


# ============== In-Memory Fallback ==============

class InMemoryFallback:
    """Simple in-process store that mimics Redis operations.

    Used when Redis is unavailable - provides basic functionality
    without persistence or distributed features.
    """

    def __init__(self):
        self._store: dict[str, Any] = {}
        self._expiry: dict[str, float] = {}

    async def get(self, key: str) -> str | None:
        """Get a key value."""
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._store[key]
            del self._expiry[key]
            return None
        return self._store.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        """Set a key value with optional expiry (seconds)."""
        self._store[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        return True

    async def delete(self, key: str) -> int:
        """Delete a key."""
        self._store.pop(key, None)
        self._expiry.pop(key, None)
        return 1

    async def exists(self, key: str) -> int:
        """Check if key exists."""
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._store[key]
            del self._expiry[key]
            return 0
        return 1 if key in self._store else 0

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiry on a key."""
        if key in self._store:
            self._expiry[key] = time.time() + seconds
            return True
        return False

    async def ttl(self, key: str) -> int:
        """Get TTL of a key (-1 if no expiry, -2 if not exists)."""
        if key not in self._store:
            return -2
        if key not in self._expiry:
            return -1
        remaining = int(self._expiry[key] - time.time())
        return max(0, remaining)

    async def hset(self, name: str, key: str, value: str) -> int:
        """Set hash field."""
        if name not in self._store:
            self._store[name] = {}
        if isinstance(self._store[name], dict):
            is_new = key not in self._store[name]
            self._store[name][key] = value
            return 1 if is_new else 0
        return 0

    async def hget(self, name: str, key: str) -> str | None:
        """Get hash field."""
        data = self._store.get(name, {})
        if isinstance(data, dict):
            return data.get(key)
        return None

    async def hgetall(self, name: str) -> dict[str, str]:
        """Get all hash fields."""
        data = self._store.get(name, {})
        if isinstance(data, dict):
            return data.copy()
        return {}

    async def hmset(self, name: str, mapping: dict[str, str]) -> bool:
        """Set multiple hash fields."""
        if name not in self._store:
            self._store[name] = {}
        if isinstance(self._store[name], dict):
            self._store[name].update(mapping)
            return True
        return False

    async def incr(self, key: str) -> int:
        """Increment a counter."""
        current = self._store.get(key, "0")
        try:
            new_val = int(current) + 1
        except ValueError:
            new_val = 1
        self._store[key] = str(new_val)
        return new_val

    async def lpush(self, key: str, *values: str) -> int:
        """Push to list (left)."""
        if key not in self._store:
            self._store[key] = []
        if not isinstance(self._store[key], list):
            self._store[key] = [self._store[key]]
        self._store[key] = list(values) + self._store[key]
        return len(self._store[key])

    async def rpop(self, key: str) -> str | None:
        """Pop from list (right)."""
        if key in self._store and isinstance(self._store[key], list):
            if self._store[key]:
                return self._store[key].pop()
        return None

    async def llen(self, key: str) -> int:
        """Get list length."""
        data = self._store.get(key, [])
        if isinstance(data, list):
            return len(data)
        return 0

    async def scan_iter(self, match: str = "*", count: int = 100) -> AsyncIterator[str]:
        """Scan keys matching pattern."""
        import fnmatch
        for k in list(self._store.keys()):
            if fnmatch.fnmatch(k, match):
                yield k

    async def keys(self, pattern: str = "*") -> list[str]:
        """Get all keys matching pattern."""
        prefix = pattern.rstrip("*")
        return [k for k in self._store.keys() if k.startswith(prefix)]

    async def ping(self) -> bool:
        """Ping check."""
        return True


_in_memory_fallback = InMemoryFallback()


def _get_client_or_fallback() -> tuple[redis.Redis | None, InMemoryFallback, bool]:
    """Get Redis client with fallback indicator.

    Returns:
        Tuple of (redis_client, fallback_store, is_fallback)
    """
    try:
        client = asyncio.get_event_loop().run_until_complete(get_redis())
        return client, _in_memory_fallback, False
    except Exception:
        return None, _in_memory_fallback, True


# ============== Distributed Lock ==============

class DistributedLock:
    """Distributed lock implementation using Redis.

    Provides mutual exclusion across multiple processes/servers.
    Uses SET NX EX pattern for atomic lock acquisition.

    Note: In fallback mode, provides no actual locking.
    """

    LOCK_PREFIX = "lock:"

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._fallback = _in_memory_fallback
        self._is_fallback = False
        self._local_locks: dict[str, str] = {}  # For fallback mode

    async def _ensure_client(self) -> tuple[Any, Any, bool]:
        """Ensure Redis client is available."""
        if self._is_fallback:
            return None, self._fallback, True
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis, self._fallback, False
        except Exception:
            self._is_fallback = True
            return None, self._fallback, True

    def _lock_key(self, name: str) -> str:
        """Generate lock key."""
        return f"{self.LOCK_PREFIX}{name}"

    async def acquire(
        self,
        name: str,
        ttl: int = 30,
        blocking: bool = False,
        blocking_timeout: int = 10,
    ) -> str | None:
        """Acquire a distributed lock.

        Args:
            name: Lock name (unique identifier)
            ttl: Lock time-to-live in seconds (auto-release)
            blocking: Wait for lock acquisition
            blocking_timeout: Max wait time if blocking

        Returns:
            Lock token (for release) if acquired, None otherwise
        """
        client, fallback, is_fb = await self._ensure_client()
        lock_key = self._lock_key(name)
        lock_token = hashlib.sha1(f"{name}:{time.time()}".encode()).hexdigest()[:16]

        if is_fb:
            # Fallback: simple in-memory lock
            if lock_key not in self._local_locks:
                self._local_locks[lock_key] = lock_token
                return lock_token
            if blocking:
                start = time.time()
                while lock_key in self._local_locks:
                    if time.time() - start > blocking_timeout:
                        return None
                    await asyncio.sleep(0.1)
                self._local_locks[lock_key] = lock_token
                return lock_token
            return None

        # Real Redis lock
        if blocking:
            start = time.time()
            while time.time() - start < blocking_timeout:
                acquired = await client.set(
                    lock_key, lock_token, nx=True, ex=ttl
                )
                if acquired:
                    return lock_token
                await asyncio.sleep(0.1)
            return None
        else:
            acquired = await client.set(lock_key, lock_token, nx=True, ex=ttl)
            return lock_token if acquired else None

    async def release(self, name: str, token: str) -> bool:
        """Release a distributed lock.

        Uses Lua script for atomic check-and-delete.

        Args:
            name: Lock name
            token: Lock token from acquire()

        Returns:
            True if released, False otherwise
        """
        client, fallback, is_fb = await self._ensure_client()
        lock_key = self._lock_key(name)

        if is_fb:
            # Fallback: simple release
            if self._local_locks.get(lock_key) == token:
                del self._local_locks[lock_key]
                return True
            return False

        # Real Redis - atomic release with Lua script
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        result = await client.eval(lua_script, 1, lock_key, token)
        return bool(result)

    async def extend(self, name: str, token: str, ttl: int = 30) -> bool:
        """Extend lock TTL.

        Args:
            name: Lock name
            token: Lock token from acquire()
            ttl: New TTL in seconds

        Returns:
            True if extended, False otherwise
        """
        client, fallback, is_fb = await self._ensure_client()
        lock_key = self._lock_key(name)

        if is_fb:
            if self._local_locks.get(lock_key) == token:
                # In fallback, just return True (no real TTL)
                return True
            return False

        # Real Redis - atomic extend with Lua script
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("expire", KEYS[1], ARGV[2])
        else
            return 0
        end
        """
        result = await client.eval(lua_script, 1, lock_key, token, ttl)
        return bool(result)

    @asynccontextmanager
    async def with_lock(self, name: str, ttl: int = 30):
        """Context manager for lock acquisition.

        Usage:
            async with distributed_lock.with_lock("my_lock"):
                # Critical section
                pass
        """
        token = await self.acquire(name, ttl, blocking=True)
        try:
            yield token
        finally:
            if token:
                await self.release(name, token)


# ============== Rate Limiter ==============

class RateLimiter:
    """Redis-based rate limiter.

    Implements sliding window algorithm for accurate rate limiting.
    """

    RATE_PREFIX = "rate:"

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._is_fallback = False

    async def _get_client(self) -> Any:
        """Get Redis client."""
        if self._is_fallback:
            return _in_memory_fallback
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis
        except Exception:
            self._is_fallback = True
            return _in_memory_fallback

    def _rate_key(self, key: str) -> str:
        """Generate rate limit key."""
        return f"{self.RATE_PREFIX}{key}"

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int = 60,
    ) -> dict[str, Any]:
        """Check if action is allowed under rate limit.

        Args:
            key: Rate limit identifier (e.g., "user:123", "ip:192.168.1.1")
            limit: Maximum allowed in window
            window: Time window in seconds (default 60)

        Returns:
            Dict with 'allowed', 'remaining', 'reset_at', 'retry_after'
        """
        client = await self._get_client()
        rate_key = self._rate_key(key)
        now = time.time()
        window_start = now - window

        # Use sliding window with sorted set
        pipe = client.pipeline() if hasattr(client, 'pipeline') else None

        if pipe:
            # Remove old entries
            await client.zremrangebyscore(rate_key, 0, window_start)
            # Count current entries
            count = await client.zcard(rate_key)
            # Add new entry
            await client.zadd(rate_key, {str(now): now})
            # Set expiry
            await client.expire(rate_key, window)
            await pipe.execute()
        else:
            # Fallback: simple counter
            count_str = await client.get(rate_key) or "0"
            try:
                count = int(count_str)
            except ValueError:
                count = 0
            if count < limit:
                await client.set(rate_key, str(count + 1), ex=window)
            else:
                count = limit  # Already at limit

        allowed = count < limit
        remaining = max(0, limit - count - (0 if allowed else 1))
        reset_at = int(now + window)

        return {
            "allowed": allowed,
            "remaining": remaining,
            "limit": limit,
            "reset_at": reset_at,
            "retry_after": 0 if allowed else window,
        }

    async def is_allowed(self, key: str, limit: int, window: int = 60) -> bool:
        """Simple check if action is allowed.

        Args:
            key: Rate limit identifier
            limit: Maximum allowed in window
            window: Time window in seconds

        Returns:
            True if allowed, False if rate limited
        """
        result = await self.check_rate_limit(key, limit, window)
        return result["allowed"]


# ============== Property Cache ==============

class PropertyCache:
    """Cache for property queries to reduce database load.

    Key features:
    - Cache property availability checks
    - Cache search results by query hash
    - Automatic invalidation on property updates
    """

    CACHE_PREFIX = "cache:property:"

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._is_fallback = False
        self._local_cache: dict[str, tuple[str, float]] = {}

    async def _get_client(self) -> Any:
        """Get Redis client."""
        if self._is_fallback:
            return _in_memory_fallback
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis
        except Exception:
            self._is_fallback = True
            return _in_memory_fallback

    def _cache_key(self, key: str) -> str:
        """Generate cache key."""
        return f"{self.CACHE_PREFIX}{key}"

    def _make_hash(self, data: dict) -> str:
        """Create hash from query parameters."""
        normalized = json.dumps(data, sort_keys=True, ensure_ascii=True)
        return hashlib.sha1(normalized.encode()).hexdigest()[:12]

    async def get_property_availability(
        self, property_ref: str
    ) -> dict[str, Any] | None:
        """Get cached property availability.

        Args:
            property_ref: Property ID or code

        Returns:
            Cached availability data or None
        """
        client = await self._get_client()
        cache_key = self._cache_key(f"availability:{property_ref}")

        if self._is_fallback:
            cached = self._local_cache.get(cache_key)
            if cached and cached[1] > time.time():
                return json.loads(cached[0])
            return None

        data = await client.get(cache_key)
        if data:
            return json.loads(data)
        return None

    async def set_property_availability(
        self,
        property_ref: str,
        data: dict[str, Any],
        ttl: int = 60,
    ) -> bool:
        """Cache property availability.

        Args:
            property_ref: Property ID or code
            data: Availability data to cache
            ttl: Cache TTL in seconds (default 60s)

        Returns:
            True if cached successfully
        """
        client = await self._get_client()
        cache_key = self._cache_key(f"availability:{property_ref}")
        payload = json.dumps(data, ensure_ascii=False)

        if self._is_fallback:
            self._local_cache[cache_key] = (payload, time.time() + ttl)
            return True

        await client.set(cache_key, payload, ex=ttl)
        return True

    async def invalidate_property(self, property_ref: str) -> bool:
        """Invalidate cache for a property.

        Called when property is updated/booked/held.

        Args:
            property_ref: Property ID or code

        Returns:
            True if invalidated
        """
        client = await self._get_client()
        cache_key = self._cache_key(f"availability:{property_ref}")

        if self._is_fallback:
            self._local_cache.pop(cache_key, None)
            return True

        await client.delete(cache_key)
        return True

    async def cache_search_results(
        self,
        query_params: dict[str, Any],
        results: list[dict],
        ttl: int = 300,
    ) -> str:
        """Cache property search results.

        Args:
            query_params: Search parameters
            results: Search results to cache
            ttl: Cache TTL in seconds (default 5 minutes)

        Returns:
            Cache key for retrieval
        """
        client = await self._get_client()
        query_hash = self._make_hash(query_params)
        cache_key = self._cache_key(f"search:{query_hash}")
        payload = json.dumps(results, ensure_ascii=False)

        if self._is_fallback:
            self._local_cache[cache_key] = (payload, time.time() + ttl)
            return query_hash

        await client.set(cache_key, payload, ex=ttl)
        return query_hash

    async def get_cached_search_results(
        self, query_params: dict[str, Any]
    ) -> list[dict] | None:
        """Get cached search results.

        Args:
            query_params: Search parameters used for cache lookup

        Returns:
            Cached results or None
        """
        client = await self._get_client()
        query_hash = self._make_hash(query_params)
        cache_key = self._cache_key(f"search:{query_hash}")

        if self._is_fallback:
            cached = self._local_cache.get(cache_key)
            if cached and cached[1] > time.time():
                return json.loads(cached[0])
            return None

        data = await client.get(cache_key)
        if data:
            return json.loads(data)
        return None

    async def clear_all(self) -> int:
        """Clear all property caches.

        Returns:
            Number of keys cleared
        """
        client = await self._get_client()
        pattern = self._cache_key("*")

        if self._is_fallback:
            count = len([k for k in self._local_cache if k.startswith(self.CACHE_PREFIX)])
            self._local_cache = {
                k: v for k, v in self._local_cache.items()
                if not k.startswith(self.CACHE_PREFIX)
            }
            return count

        count = 0
        async for key in client.scan_iter(match=pattern):
            await client.delete(key)
            count += 1
        return count


# ============== Session Memory ==============

class RedisSessionMemory:
    """Redis-backed session memory.

    Extends the existing ShortTermMemory concept with Redis storage.
    """

    SESSION_PREFIX = "session:"
    SESSION_TTL = 3600  # 1 hour default

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._is_fallback = False

    async def _get_client(self) -> Any:
        """Get Redis client."""
        if self._is_fallback:
            return _in_memory_fallback
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis
        except Exception:
            self._is_fallback = True
            return _in_memory_fallback

    def _session_key(self, session_id: str) -> str:
        """Get Redis key for session."""
        return f"{self.SESSION_PREFIX}{session_id}"

    async def save_session(
        self,
        session_id: str,
        messages: list[dict],
        metadata: dict | None = None,
        ttl: int = SESSION_TTL,
    ) -> None:
        """Save session data.

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

        await client.hmset(key, data)
        await client.expire(key, ttl)
        logger.debug(f"Saved session {session_id} with TTL {ttl}s")

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get session data.

        Args:
            session_id: Session identifier

        Returns:
            Session data dict or None
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

    async def delete_session(self, session_id: str) -> None:
        """Delete a session.

        Args:
            session_id: Session identifier
        """
        client = await self._get_client()
        key = self._session_key(session_id)
        await client.delete(key)
        logger.debug(f"Deleted session {session_id}")

    async def session_exists(self, session_id: str) -> bool:
        """Check if session exists.

        Args:
            session_id: Session identifier

        Returns:
            True if session exists
        """
        client = await self._get_client()
        key = self._session_key(session_id)
        return await client.exists(key) > 0

    async def list_sessions(self, customer_id: str) -> list[dict[str, Any]]:
        """Return only sessions owned by a customer."""
        client = await self._get_client()
        sessions: list[dict[str, Any]] = []
        async for key in client.scan_iter(match=f"{self.SESSION_PREFIX}*"):
            key_text = key.decode("utf-8") if isinstance(key, bytes) else key
            session_id = key_text.removeprefix(self.SESSION_PREFIX)
            data = await self.get_session(session_id)
            if not data:
                continue
            metadata = data.get("metadata", {})
            if str(metadata.get("customer_id")) != str(customer_id):
                continue
            messages = data.get("messages", [])
            first_user = next(
                (m.get("content", "") for m in messages if m.get("role", "").lower() == "user"),
                "Cuộc trò chuyện mới",
            )
            sessions.append({
                "session_id": session_id,
                "preview": first_user[:50] + ("..." if len(first_user) > 50 else ""),
                "message_count": len(messages),
                "last_active": metadata.get("last_active", ""),
            })
        sessions.sort(key=lambda item: item.get("last_active", ""), reverse=True)
        return sessions


# ============== Message Queue ==============

class MessageQueue:
    """Simple Redis-based message queue.

    Provides FIFO queue operations for background job processing.
    """

    QUEUE_PREFIX = "queue:"

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._is_fallback = False

    async def _get_client(self) -> Any:
        """Get Redis client."""
        if self._is_fallback:
            return _in_memory_fallback
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis
        except Exception:
            self._is_fallback = True
            return _in_memory_fallback

    def _queue_key(self, queue_name: str) -> str:
        """Get queue key."""
        return f"{self.QUEUE_PREFIX}{queue_name}"

    async def enqueue(self, queue_name: str, message: dict[str, Any]) -> bool:
        """Add message to queue.

        Args:
            queue_name: Name of the queue
            message: Message payload (will be JSON serialized)

        Returns:
            True if enqueued successfully
        """
        client = await self._get_client()
        key = self._queue_key(queue_name)
        payload = json.dumps(message, ensure_ascii=False)

        await client.lpush(key, payload)
        logger.debug(f"Enqueued message to {queue_name}")
        return True

    async def dequeue(self, queue_name: str) -> dict[str, Any] | None:
        """Get next message from queue.

        Uses blocking pop for efficient waiting.

        Args:
            queue_name: Name of the queue

        Returns:
            Message payload or None if queue empty
        """
        client = await self._get_client()
        key = self._queue_key(queue_name)

        if self._is_fallback:
            # Simple non-blocking pop for fallback
            data = await client.rpop(key)
            if data:
                return json.loads(data)
            return None

        # Use BRPOP for blocking
        result = await client.brpop(key, timeout=1)
        if result:
            _, data = result
            return json.loads(data)
        return None

    async def get_length(self, queue_name: str) -> int:
        """Get queue length.

        Args:
            queue_name: Name of the queue

        Returns:
            Number of messages in queue
        """
        client = await self._get_client()
        key = self._queue_key(queue_name)
        return await client.llen(key)

    async def peek(self, queue_name: str, count: int = 10) -> list[dict[str, Any]]:
        """Peek at messages without removing.

        Args:
            queue_name: Name of the queue
            count: Max messages to peek

        Returns:
            List of messages (oldest first)
        """
        client = await self._get_client()
        key = self._queue_key(queue_name)

        messages = []
        for _ in range(count):
            data = await client.rpop(key)
            if not data:
                break
            messages.append(json.loads(data))
            # Re-push for peek
            await client.lpush(key, data)

        return messages


# ============== Pub/Sub ==============

class EventPubSub:
    """Redis Pub/Sub for real-time events.

    Supports:
    - Direct channel subscriptions
    - Pattern-based subscriptions
    - Async event handling
    """

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._pubsub: redis.client.PubSub | None = None

    async def _ensure_redis(self) -> redis.Redis:
        """Ensure Redis client is available."""
        if self._redis is None:
            self._redis = await get_redis()
        return self._redis

    async def publish(self, channel: str, event: dict[str, Any]) -> int:
        """Publish event to channel.

        Args:
            channel: Channel name
            event: Event payload

        Returns:
            Number of subscribers that received the message
        """
        client = await self._ensure_redis()
        payload = json.dumps(event, ensure_ascii=False)
        return await client.publish(channel, payload)

    async def subscribe(self, channel: str) -> AsyncIterator[dict[str, Any]]:
        """Subscribe to channel and yield events.

        Usage:
            async for event in pubsub.subscribe("my_channel"):
                print(event)

        Args:
            channel: Channel name

        Yields:
            Event payloads
        """
        client = await self._ensure_redis()
        pubsub = client.pubsub()
        await pubsub.subscribe(channel)

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield json.loads(message["data"])
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

    async def psubscribe(self, pattern: str) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        """Subscribe to pattern and yield matching events.

        Usage:
            async for channel, event in pubsub.psubscribe("user:*"):
                print(f"Event on {channel}:", event)

        Args:
            pattern: Pattern to match (e.g., "user:*")

        Yields:
            Tuples of (channel, event_payload)
        """
        client = await self._ensure_redis()
        pubsub = client.pubsub()
        await pubsub.psubscribe(pattern)

        try:
            async for message in pubsub.listen():
                if message["type"] == "pmessage":
                    yield message["channel"], json.loads(message["data"])
        finally:
            await pubsub.punsubscribe(pattern)
            await pubsub.close()


# ============== Property Hold Manager ==============

class PropertyHoldManager:
    """Manages temporary holds on properties.

    Provides distributed hold management so multiple agents
    can't book the same property simultaneously.
    """

    HOLD_PREFIX = "hold:property:"

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._is_fallback = False
        self._local_holds: dict[str, dict] = {}

    async def _get_client(self) -> Any:
        """Get Redis client."""
        if self._is_fallback:
            return _in_memory_fallback
        try:
            if self._redis is None:
                self._redis = await get_redis()
            await self._redis.ping()
            return self._redis
        except Exception:
            self._is_fallback = True
            return _in_memory_fallback

    def _hold_key(self, property_id: str) -> str:
        """Get hold key for property."""
        return f"{self.HOLD_PREFIX}{property_id}"

    async def acquire_hold(
        self,
        property_id: str,
        customer_id: str,
        ttl: int = 900,
    ) -> str | None:
        """Acquire a hold on a property.

        Args:
            property_id: Property UUID
            customer_id: Customer UUID requesting hold
            ttl: Hold duration in seconds (default 15 minutes)

        Returns:
            Hold ID if acquired, None if already held
        """
        client = await self._get_client()
        hold_key = self._hold_key(property_id)

        # Check if already held
        existing = await client.get(hold_key)
        if existing:
            hold_data = json.loads(existing)
            if hold_data["expires_at"] > time.time():
                # Already held
                return None
            # Expired, can acquire

        hold_id = hashlib.sha1(f"{property_id}:{customer_id}:{time.time()}".encode()).hexdigest()[:12]
        hold_data = {
            "hold_id": hold_id,
            "property_id": property_id,
            "customer_id": customer_id,
            "acquired_at": time.time(),
            "expires_at": time.time() + ttl,
            "ttl": ttl,
        }

        if self._is_fallback:
            self._local_holds[hold_key] = hold_data
            return hold_id

        # Use SET NX to ensure atomic acquisition
        success = await client.set(
            hold_key,
            json.dumps(hold_data),
            nx=True,
            ex=ttl + 60,  # Extra buffer for cleanup
        )

        if success:
            return hold_id
        return None

    async def release_hold(self, property_id: str, hold_id: str) -> bool:
        """Release a hold on a property.

        Args:
            property_id: Property UUID
            hold_id: Hold ID from acquire_hold

        Returns:
            True if released, False otherwise
        """
        client = await self._get_client()
        hold_key = self._hold_key(property_id)

        if self._is_fallback:
            existing = self._local_holds.get(hold_key)
            if existing and existing["hold_id"] == hold_id:
                del self._local_holds[hold_key]
                return True
            return False

        # Verify hold_id matches before deleting
        existing = await client.get(hold_key)
        if existing:
            hold_data = json.loads(existing)
            if hold_data["hold_id"] == hold_id:
                await client.delete(hold_key)
                return True
        return False

    async def get_hold_status(self, property_id: str) -> dict[str, Any] | None:
        """Get current hold status for a property.

        Args:
            property_id: Property UUID

        Returns:
            Hold info dict or None if not held
        """
        client = await self._get_client()
        hold_key = self._hold_key(property_id)

        if self._is_fallback:
            existing = self._local_holds.get(hold_key)
            if existing and existing["expires_at"] > time.time():
                remaining = int(existing["expires_at"] - time.time())
                return {
                    **existing,
                    "is_active": True,
                    "remaining_seconds": remaining,
                }
            return {"is_active": False}

        data = await client.get(hold_key)
        if not data:
            return {"is_active": False}

        hold_data = json.loads(data)
        if hold_data["expires_at"] < time.time():
            # Expired
            return {"is_active": False}

        remaining = int(hold_data["expires_at"] - time.time())
        return {
            **hold_data,
            "is_active": True,
            "remaining_seconds": remaining,
        }

    async def extend_hold(
        self, property_id: str, hold_id: str, additional_ttl: int = 900
    ) -> bool:
        """Extend an existing hold.

        Args:
            property_id: Property UUID
            hold_id: Hold ID from acquire_hold
            additional_ttl: Additional time in seconds

        Returns:
            True if extended, False otherwise
        """
        client = await self._get_client()
        hold_key = self._hold_key(property_id)

        if self._is_fallback:
            existing = self._local_holds.get(hold_key)
            if existing and existing["hold_id"] == hold_id:
                existing["expires_at"] += additional_ttl
                existing["ttl"] = additional_ttl
                return True
            return False

        # Get current hold
        data = await client.get(hold_key)
        if not data:
            return False

        hold_data = json.loads(data)
        if hold_data["hold_id"] != hold_id:
            return False

        # Update expiry
        hold_data["expires_at"] = time.time() + additional_ttl
        hold_data["ttl"] = additional_ttl

        # Get remaining TTL and update
        current_ttl = await client.ttl(hold_key)
        await client.set(
            hold_key,
            json.dumps(hold_data),
            ex=max(current_ttl, additional_ttl + 60),
        )
        return True

    async def is_available(self, property_id: str) -> bool:
        """Check if property is available (not held).

        Args:
            property_id: Property UUID

        Returns:
            True if available, False if held
        """
        status = await self.get_hold_status(property_id)
        return not status.get("is_active", False)


# ============== Singleton Instances ==============

_distributed_lock: DistributedLock | None = None
_rate_limiter: RateLimiter | None = None
_property_cache: PropertyCache | None = None
_session_memory: RedisSessionMemory | None = None
_message_queue: MessageQueue | None = None
_event_pubsub: EventPubSub | None = None
_property_hold_manager: PropertyHoldManager | None = None


def get_distributed_lock() -> DistributedLock:
    """Get distributed lock singleton."""
    global _distributed_lock
    if _distributed_lock is None:
        _distributed_lock = DistributedLock()
    return _distributed_lock


def get_rate_limiter() -> RateLimiter:
    """Get rate limiter singleton."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


def get_property_cache() -> PropertyCache:
    """Get property cache singleton."""
    global _property_cache
    if _property_cache is None:
        _property_cache = PropertyCache()
    return _property_cache


def get_session_memory() -> RedisSessionMemory:
    """Get session memory singleton."""
    global _session_memory
    if _session_memory is None:
        _session_memory = RedisSessionMemory()
    return _session_memory


def get_message_queue() -> MessageQueue:
    """Get message queue singleton."""
    global _message_queue
    if _message_queue is None:
        _message_queue = MessageQueue()
    return _message_queue


def get_event_pubsub() -> EventPubSub:
    """Get event pub/sub singleton."""
    global _event_pubsub
    if _event_pubsub is None:
        _event_pubsub = EventPubSub()
    return _event_pubsub


def get_property_hold_manager() -> PropertyHoldManager:
    """Get property hold manager singleton."""
    global _property_hold_manager
    if _property_hold_manager is None:
        _property_hold_manager = PropertyHoldManager()
    return _property_hold_manager
