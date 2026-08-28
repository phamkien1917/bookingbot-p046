import time
from unittest.mock import patch

import pytest

from src.services.redis_service import (
    DistributedLock,
    InMemoryFallback,
    PropertyCache,
    PropertyHoldManager,
    RateLimiter,
    is_redis_available,
)


@pytest.mark.asyncio
async def test_in_memory_fallback_get_set():
    store = InMemoryFallback()

    await store.set("test_key", "test_value")
    assert await store.get("test_key") == "test_value"

    await store.set("temp_key", "temp_value", ex=1)
    assert await store.get("temp_key") == "temp_value"

    # Simulate time pass
    store._expiry["temp_key"] = time.time() - 1
    assert await store.get("temp_key") is None


@pytest.mark.asyncio
async def test_in_memory_fallback_delete_and_exists():
    store = InMemoryFallback()
    await store.set("k1", "v1")

    assert await store.exists("k1") == 1
    assert await store.exists("k3") == 0

    assert await store.delete("k1") == 1
    assert await store.delete("k3") == 0
    assert await store.get("k1") is None


@pytest.mark.asyncio
async def test_in_memory_fallback_list_operations():
    store = InMemoryFallback()

    await store.lpush("my_list", "msg1", "msg2")
    assert await store.llen("my_list") == 2

    # lpush prepends, so rpop returns the oldest message first
    assert await store.rpop("my_list") == "msg1"
    assert await store.rpop("my_list") == "msg2"
    assert await store.rpop("my_list") is None
    assert await store.llen("my_list") == 0


@pytest.mark.asyncio
async def test_in_memory_fallback_incr():
    store = InMemoryFallback()
    assert await store.incr("counter") == 1
    assert await store.incr("counter") == 2


@pytest.mark.asyncio
async def test_distributed_lock_fallback():
    lock = DistributedLock()
    lock._is_fallback = True

    token = await lock.acquire("resource:1", ttl=5)
    assert token is not None

    # Same lock name cannot be acquired twice before release
    assert await lock.acquire("resource:1", ttl=5) is None

    assert await lock.release("resource:1", token) is True
    assert await lock.acquire("resource:1", ttl=5) is not None


@pytest.mark.asyncio
async def test_rate_limiter_fallback():
    limiter = RateLimiter()
    limiter._is_fallback = True
    key = f"user:rate:{time.time()}"

    assert await limiter.is_allowed(key, limit=3) is True
    assert await limiter.is_allowed(key, limit=3) is True
    assert await limiter.is_allowed(key, limit=3) is True

    # Fourth call in the same window exceeds the limit
    assert await limiter.is_allowed(key, limit=3) is False


def test_property_cache_hash_is_order_independent():
    cache = PropertyCache()
    key1 = cache._make_hash({"city": "ha_noi", "min_price": 1000, "max_price": 3000})
    key2 = cache._make_hash({"max_price": 3000, "city": "ha_noi", "min_price": 1000})
    assert key1 == key2


@pytest.mark.asyncio
async def test_property_hold_manager_fallback():
    mgr = PropertyHoldManager()
    mgr._is_fallback = True
    prop_id = "prop_12345"

    hold_id = await mgr.acquire_hold(prop_id, "user_99999", ttl=900)
    assert hold_id is not None
    assert (await mgr.get_hold_status(prop_id))["is_active"] is True

    # A second customer must not get a hold on the same property
    assert await mgr.acquire_hold(prop_id, "user_00001", ttl=900) is None

    assert await mgr.release_hold(prop_id, hold_id) is True
    assert (await mgr.get_hold_status(prop_id))["is_active"] is False


@pytest.mark.asyncio
async def test_is_redis_available_handles_exception():
    with patch("src.services.redis_service.get_redis", side_effect=Exception("Redis down")):
        assert await is_redis_available() is False
