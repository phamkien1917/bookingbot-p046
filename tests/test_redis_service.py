import asyncio
import time
import pytest
from unittest.mock import AsyncMock, patch

from src.services.redis_service import (
    InMemoryFallback,
    DistributedLock,
    RateLimiter,
    PropertyCache,
    PropertyHoldManager,
    is_redis_available,
)


@pytest.mark.asyncio
async def test_in_memory_fallback_get_set():
    store = InMemoryFallback()
    
    # Set and get
    await store.set("test_key", "test_value")
    val = await store.get("test_key")
    assert val == "test_value"
    
    # Expiry test
    await store.set("temp_key", "temp_value", ex=1)
    assert await store.get("temp_key") == "temp_value"
    
    # Simulate time pass
    store._expiry["temp_key"] = time.time() - 1
    assert await store.get("temp_key") is None


@pytest.mark.asyncio
async def test_in_memory_fallback_delete_and_exists():
    store = InMemoryFallback()
    await store.set("k1", "v1")
    await store.set("k2", "v2")
    
    assert await store.exists("k1") == 1
    assert await store.exists("k3") == 0
    
    del_count = await store.delete("k1", "k2", "k3")
    assert del_count == 2
    assert await store.get("k1") is None


@pytest.mark.asyncio
async def test_in_memory_fallback_list_operations():
    store = InMemoryFallback()
    
    # lpush
    await store.lpush("my_list", "msg1", "msg2")
    
    # lrange
    items = await store.lrange("my_list", 0, -1)
    assert len(items) == 2
    assert items[0] == "msg2"  # lpush prepends
    
    # ltrim
    await store.ltrim("my_list", 0, 0)
    trimmed = await store.lrange("my_list", 0, -1)
    assert len(trimmed) == 1
    assert trimmed[0] == "msg2"


@pytest.mark.asyncio
async def test_in_memory_fallback_incr():
    store = InMemoryFallback()
    val1 = await store.incr("counter")
    assert val1 == 1
    val2 = await store.incr("counter")
    assert val2 == 2


@pytest.mark.asyncio
async def test_distributed_lock_fallback():
    lock = DistributedLock("lock:resource:1", ttl=5)
    
    # Acquire lock
    acquired = await lock.acquire()
    assert acquired is True
    assert lock.is_locked() is True
    
    # Trying to acquire same lock with another instance should fail
    lock2 = DistributedLock("lock:resource:1", ttl=5)
    acquired2 = await lock2.acquire()
    assert acquired2 is False
    
    # Release lock
    await lock.release()
    assert lock.is_locked() is False
    
    # Now lock2 can acquire
    assert await lock2.acquire() is True
    await lock2.release()


@pytest.mark.asyncio
async def test_rate_limiter_fallback():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    key = "user:rate:test"
    
    # First 3 requests succeed
    assert await limiter.is_allowed(key) is True
    assert await limiter.is_allowed(key) is True
    assert await limiter.is_allowed(key) is True
    
    # 4th request exceeds rate limit
    assert await limiter.is_allowed(key) is False


@pytest.mark.asyncio
async def test_property_cache_generation():
    cache = PropertyCache(ttl=300)
    key1 = cache._make_key("ha_noi", min_price=1000, max_price=3000)
    key2 = cache._make_key("ha_noi", max_price=3000, min_price=1000)
    # Order of kwargs shouldn't change hash
    assert key1 == key2


@pytest.mark.asyncio
async def test_property_hold_manager():
    mgr = PropertyHoldManager(hold_duration_minutes=15)
    prop_id = "prop_12345"
    user_id = "user_99999"
    
    # Hold property
    held = await mgr.hold_property(prop_id, user_id, slot_time="09:00-10:00")
    assert held is True
    
    # Check is_held
    assert await mgr.is_held(prop_id, slot_time="09:00-10:00") is True
    
    # Release hold
    await mgr.release_hold(prop_id, slot_time="09:00-10:00")
    assert await mgr.is_held(prop_id, slot_time="09:00-10:00") is False


@pytest.mark.asyncio
async def test_is_redis_available_handles_exception():
    with patch("src.services.redis_service.get_redis", side_effect=Exception("Redis down")):
        available = await is_redis_available()
        assert available is False
