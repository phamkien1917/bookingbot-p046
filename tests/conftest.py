"""Shared pytest fixtures.

Two things every API test needs and should not rebuild: an HTTP client that
speaks to the app in-process, and a guarantee that one test's database engine
does not leak into the next one's event loop.

Nothing here reaches the network. The endpoints under test run against
overridden dependencies and a stubbed agent, so the suite stays free of a
database, a Redis and an LLM bill.
"""

from __future__ import annotations

from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.api.routes import auth as auth_module
from src.database import get_session
from src.database.connection import close_engine
from src.main import app


@pytest_asyncio.fixture(autouse=True)
async def _dispose_db_engine():
    """Drop the SQLAlchemy engine after every test.

    connection.py already selects NullPool under test, but an asyncpg background
    task can still hold a reference to the loop that just closed. Disposing makes
    the next test start from nothing.
    """
    yield
    try:
        await close_engine()
    except Exception:  # the engine may never have been created in this test
        pass


@pytest_asyncio.fixture
async def client():
    """An anonymous caller, with no database behind it.

    ASGITransport hands the request straight to the app object, so there is no
    socket and no server process - the same request path, minus the wait.
    """

    async def _no_db() -> Any:
        yield None

    app.dependency_overrides[get_session] = _no_db
    app.dependency_overrides[auth_module.get_optional_current_user] = lambda: None
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def fake_run_agent():
    """Build a stand-in for run_agent that returns a chosen final state.

    The endpoint's job is to turn an AgentState into a ChatResponse. Replacing
    the graph keeps the test on that contract rather than on whatever the model
    felt like saying that day.
    """

    def build(response: str = "Chao ban.", **overrides: Any):
        nodes = overrides.pop("nodes", None) or []

        async def _run(state: dict[str, Any], on_stage: Any = None) -> dict[str, Any]:
            for node in nodes:
                if on_stage:
                    on_stage(node)
            return {
                **state,
                "response": response,
                "response_kind": "DIRECT",
                "intent": "GREETING",
                "ai_mode": "llm_direct",
                "ai_model": "test-model",
                "ai_latency_ms": 5,
                "suggested_actions": [],
                **overrides,
            }

        return _run

    return build


@pytest.fixture
def sample_chat_request():
    """A request in the domain this product actually serves."""
    return {"message": "Tìm căn hộ 2 phòng ngủ ở Cầu Giấy dưới 5 tỷ"}
