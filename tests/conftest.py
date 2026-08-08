"""Pytest configuration — autouse dispose DB engine sau mỗi test.

Race condition fix: Kết hợp 2 lớp bảo vệ:

1. `connection.py` tự detect test env → dùng NullPool (mỗi session connection mới).
2. `conftest.py` autouse fixture gọi `engine.dispose()` cuối mỗi test →
   reset hoàn toàn, đảm bảo loop cũ không giữ connection sang loop mới.
"""

from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.database.connection import close_engine


@pytest_asyncio.fixture(autouse=True)
async def _dispose_db_engine():
    """Dispose SQLAlchemy async engine sau MỖI test.

    Đây là lớp bảo vệ thứ 2 (sau NullPool trong connection.py):
    dù NullPool đã tránh pool cache, một số task asyncpg background
    vẫn có thể giữ reference đến loop cũ. Dispose() ép tất cả về None.
    """
    yield
    try:
        await close_engine()
    except Exception:
        pass  # engine có thể chưa được tạo trong test này


@pytest_asyncio.fixture
async def client():
    """Async HTTP client for testing API endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_llm():
    """Mock LLM to avoid calling OpenAI during tests.

    Usage in test:
        def test_something(mock_llm):
            # LLM calls will return mock response instead of hitting OpenAI
            ...
    """
    mock = AsyncMock()
    mock.ainvoke.return_value = AsyncMock(content="Mocked LLM response")
    return mock
