"""Every Redis-backed service, exercised with Redis absent.

The product claims Redis is optional: lose it and conversations keep their
state, holds keep working, the rate limiter keeps counting. That claim is a
resilience promise made to a customer mid-booking, and until now only three of
the seven services had a test behind it.

Each class carries an `_is_fallback` flag and an in-process store. Setting the
flag is exactly what `_get_client_or_fallback()` does when the connection fails,
so these run the same code path a real outage produces — no mock of Redis, no
Redis, and no assertion that a mock was called.
"""

import asyncio
import time

import pytest

from src.services.redis_service import (
    DistributedLock,
    EventPubSub,
    InMemoryFallback,
    MessageQueue,
    PropertyCache,
    PropertyHoldManager,
    RateLimiter,
    RedisSessionMemory,
    get_distributed_lock,
    get_event_pubsub,
    get_message_queue,
    get_property_cache,
    get_property_hold_manager,
    get_rate_limiter,
    get_session_memory,
)


def fallback(cls):
    """Build a service in the state a Redis outage puts it in."""
    service = cls()
    service._is_fallback = True
    return service


# ── The store underneath everything ──────────────────────────────────────────


class TestInMemoryFallback:
    @pytest.mark.asyncio
    async def test_a_key_expires_when_its_ttl_passes(self):
        store = InMemoryFallback()
        await store.set("k", "v", ex=1)
        assert await store.get("k") == "v"

        store._expiry["k"] = time.time() - 1  # travel past the deadline

        assert await store.get("k") is None
        assert await store.exists("k") == 0

    @pytest.mark.asyncio
    async def test_delete_reports_whether_the_key_was_there(self):
        """Redis DEL returns a count; callers branch on it."""
        store = InMemoryFallback()
        await store.set("k", "v")

        assert await store.delete("k") == 1
        assert await store.delete("k") == 0

    @pytest.mark.asyncio
    async def test_expire_only_applies_to_a_key_that_exists(self):
        store = InMemoryFallback()

        assert await store.expire("missing", 10) is False

        await store.set("k", "v")
        assert await store.expire("k", 10) is True

    @pytest.mark.asyncio
    async def test_ttl_distinguishes_no_expiry_from_no_key(self):
        """-1 and -2 mean different things; collapsing them hides a bug."""
        store = InMemoryFallback()
        await store.set("forever", "v")

        assert await store.ttl("forever") == -1
        assert await store.ttl("never-set") == -2


# ── Locking ──────────────────────────────────────────────────────────────────


class TestDistributedLock:
    @pytest.mark.asyncio
    async def test_a_lock_is_not_released_by_the_wrong_token(self):
        """Otherwise any caller could free another caller's lock."""
        lock = fallback(DistributedLock)
        token = await lock.acquire("prop:1", ttl=5)

        assert await lock.release("prop:1", "not-my-token") is False
        assert await lock.acquire("prop:1", ttl=5) is None, "the lock was freed anyway"

        assert await lock.release("prop:1", token) is True

    @pytest.mark.asyncio
    async def test_two_different_names_do_not_block_each_other(self):
        lock = fallback(DistributedLock)

        assert await lock.acquire("prop:1", ttl=5) is not None
        assert await lock.acquire("prop:2", ttl=5) is not None

    @pytest.mark.asyncio
    async def test_the_key_is_namespaced(self):
        """A bare property id would collide with every other kind of key."""
        lock = fallback(DistributedLock)

        assert lock._lock_key("prop:1") != "prop:1"
        assert "prop:1" in lock._lock_key("prop:1")


# ── Rate limiting ────────────────────────────────────────────────────────────


class TestRateLimiter:
    @pytest.mark.asyncio
    async def test_two_callers_are_counted_separately(self):
        """A shared counter would let one busy user lock everyone else out."""
        limiter = fallback(RateLimiter)
        busy = f"user:busy:{time.time()}"
        quiet = f"user:quiet:{time.time()}"

        for _ in range(3):
            assert await limiter.is_allowed(busy, limit=3) is True
        assert await limiter.is_allowed(busy, limit=3) is False

        assert await limiter.is_allowed(quiet, limit=3) is True

    @pytest.mark.asyncio
    async def test_check_reports_what_is_left(self):
        limiter = fallback(RateLimiter)
        key = f"user:count:{time.time()}"

        info = await limiter.check_rate_limit(key, limit=5)

        assert info["allowed"] is True
        assert info["limit"] == 5
        assert info["remaining"] < 5, "a consumed request was not counted"
        assert info["retry_after"] == 0


# ── Caching ──────────────────────────────────────────────────────────────────


class TestPropertyCache:
    @pytest.mark.asyncio
    async def test_availability_survives_a_round_trip(self):
        cache = fallback(PropertyCache)
        payload = {"status": "AVAILABLE", "slots": [9, 14]}

        await cache.set_property_availability("prop-1", payload, ttl=60)

        assert await cache.get_property_availability("prop-1") == payload

    @pytest.mark.asyncio
    async def test_invalidation_actually_clears_the_entry(self):
        """A stale availability is how two customers get offered one slot."""
        cache = fallback(PropertyCache)
        await cache.set_property_availability("prop-1", {"status": "AVAILABLE"}, ttl=60)

        await cache.invalidate_property("prop-1")

        assert await cache.get_property_availability("prop-1") is None

    @pytest.mark.asyncio
    async def test_a_different_query_does_not_read_another_query_result(self):
        cache = fallback(PropertyCache)
        await cache.cache_search_results({"district": "Cầu Giấy"}, [{"id": "a"}], ttl=60)

        assert await cache.get_cached_search_results({"district": "Ba Đình"}) is None
        assert await cache.get_cached_search_results({"district": "Cầu Giấy"}) == [{"id": "a"}]

    @pytest.mark.asyncio
    async def test_a_never_cached_query_returns_nothing_rather_than_empty(self):
        """None means "not cached"; [] would mean "no properties match"."""
        cache = fallback(PropertyCache)

        assert await cache.get_cached_search_results({"district": "Chưa từng hỏi"}) is None

    def test_the_hash_ignores_key_order_but_not_values(self):
        cache = PropertyCache()

        assert cache._make_hash({"a": 1, "b": 2}) == cache._make_hash({"b": 2, "a": 1})
        assert cache._make_hash({"a": 1}) != cache._make_hash({"a": 2})


# ── Conversation state ───────────────────────────────────────────────────────


class TestRedisSessionMemory:
    @pytest.mark.asyncio
    async def test_a_conversation_is_returned_the_way_it_was_saved(self):
        memory = fallback(RedisSessionMemory)
        messages = [
            {"role": "user", "content": "Tìm căn 2PN Cầu Giấy"},
            {"role": "assistant", "content": "Mình tìm được 3 căn."},
        ]

        await memory.save_session("s1", messages, {"customer_id": "c1"})
        session = await memory.get_session("s1")

        assert session["messages"] == messages
        assert session["metadata"]["customer_id"] == "c1"

    @pytest.mark.asyncio
    async def test_an_unknown_session_is_absent_not_empty(self):
        memory = fallback(RedisSessionMemory)

        assert await memory.get_session("never-existed") is None
        assert await memory.session_exists("never-existed") is False

    @pytest.mark.asyncio
    async def test_deleting_a_session_removes_it(self):
        memory = fallback(RedisSessionMemory)
        await memory.save_session("s1", [{"role": "user", "content": "hi"}])

        await memory.delete_session("s1")

        assert await memory.session_exists("s1") is False

    @pytest.mark.asyncio
    async def test_saving_again_replaces_rather_than_appends(self):
        """Otherwise a long chat doubles every time it is written back."""
        memory = fallback(RedisSessionMemory)
        await memory.save_session("s1", [{"role": "user", "content": "một"}])
        await memory.save_session("s1", [{"role": "user", "content": "hai"}])

        assert len((await memory.get_session("s1"))["messages"]) == 1


# ── Queue ────────────────────────────────────────────────────────────────────


class TestMessageQueue:
    """The in-memory store is a module singleton, so each test needs its own name."""

    @pytest.mark.asyncio
    async def test_messages_come_back_in_the_order_they_went_in(self):
        queue = fallback(MessageQueue)
        name = f"order-{time.time()}"
        for n in range(3):
            await queue.enqueue(name, {"n": n})

        assert (await queue.dequeue(name))["n"] == 0
        assert (await queue.dequeue(name))["n"] == 1

    @pytest.mark.asyncio
    async def test_an_empty_queue_yields_nothing_instead_of_blocking(self):
        queue = fallback(MessageQueue)
        name = f"empty-{time.time()}"

        assert await queue.dequeue(name) is None
        assert await queue.get_length(name) == 0

    @pytest.mark.asyncio
    async def test_peek_looks_without_consuming(self):
        queue = fallback(MessageQueue)
        name = f"peek-{time.time()}"
        await queue.enqueue(name, {"n": 1})

        seen = await queue.peek(name, count=5)

        assert await queue.get_length(name) == 1, "peek ate the message"
        assert seen == [{"n": 1}]

    @pytest.mark.asyncio
    async def test_peek_does_not_reorder_the_queue(self):
        """The old implementation popped from the tail and pushed to the head."""
        queue = fallback(MessageQueue)
        name = f"reorder-{time.time()}"
        for n in range(3):
            await queue.enqueue(name, {"n": n})

        await queue.peek(name, count=3)

        assert (await queue.dequeue(name))["n"] == 0, "peek changed who is next"


# ── Pub/sub ──────────────────────────────────────────────────────────────────


class TestEventPubSub:
    @pytest.mark.asyncio
    async def test_publishing_without_redis_is_survivable(self):
        """Notifications are best-effort; losing Redis must not fail a booking."""
        events = fallback(EventPubSub)

        await events.publish("booking.confirmed", {"id": "b1"})


# ── Holds ────────────────────────────────────────────────────────────────────


class TestPropertyHoldManager:
    @pytest.mark.asyncio
    async def test_a_second_customer_cannot_take_a_held_property(self):
        manager = fallback(PropertyHoldManager)
        await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        assert await manager.acquire_hold("prop-1", "customer-b", ttl=900) is None
        assert await manager.is_available("prop-1") is False

    @pytest.mark.asyncio
    async def test_a_released_property_is_available_again(self):
        manager = fallback(PropertyHoldManager)
        hold = await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        assert await manager.release_hold("prop-1", hold) is True
        assert await manager.is_available("prop-1") is True

    @pytest.mark.asyncio
    async def test_the_wrong_hold_id_cannot_release_someone_else_s_hold(self):
        manager = fallback(PropertyHoldManager)
        await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        assert await manager.release_hold("prop-1", "guessed-id") is False
        assert await manager.is_available("prop-1") is False

    @pytest.mark.asyncio
    async def test_status_names_the_holder(self):
        manager = fallback(PropertyHoldManager)
        await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        status = await manager.get_hold_status("prop-1")

        assert status["is_active"] is True
        assert "customer-a" in str(status)

    @pytest.mark.asyncio
    async def test_extending_keeps_the_hold_with_the_same_owner(self):
        manager = fallback(PropertyHoldManager)
        hold = await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        await manager.extend_hold("prop-1", hold, additional_ttl=300)

        assert (await manager.get_hold_status("prop-1"))["is_active"] is True
        assert await manager.acquire_hold("prop-1", "customer-b", ttl=900) is None

    @pytest.mark.asyncio
    async def test_two_properties_are_held_independently(self):
        manager = fallback(PropertyHoldManager)
        await manager.acquire_hold("prop-1", "customer-a", ttl=900)

        assert await manager.acquire_hold("prop-2", "customer-b", ttl=900) is not None

    @pytest.mark.asyncio
    async def test_concurrent_requests_leave_exactly_one_winner(self):
        """The whole point of the hold: one property, one holder."""
        manager = fallback(PropertyHoldManager)

        results = await asyncio.gather(
            *(manager.acquire_hold("prop-1", f"customer-{n}", ttl=900) for n in range(8))
        )

        assert len([r for r in results if r]) == 1


# ── Singletons ───────────────────────────────────────────────────────────────


def test_each_accessor_returns_one_shared_instance():
    """A per-call instance would give every request its own lock table."""
    for accessor in (
        get_distributed_lock,
        get_rate_limiter,
        get_property_cache,
        get_session_memory,
        get_message_queue,
        get_event_pubsub,
        get_property_hold_manager,
    ):
        assert accessor() is accessor(), f"{accessor.__name__} builds a new object each call"
