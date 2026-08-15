"""Database connection and session management.

Supports both PostgreSQL (production) and SQLite (development).

Race condition fix: Khi chạy pytest, dùng NullPool để tránh
"Event loop is closed" / "attached to different loop" khi pytest-asyncio
tạo loop mới cho mỗi test. Production vẫn dùng AsyncAdaptedQueuePool (mặc định).
"""

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from src.config import get_settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


def _get_database_url() -> str:
    """Get the database URL from settings.

    Handles both sync and async database drivers.
    """
    settings = get_settings()
    url = settings.database_url

    # Convert sync drivers to async
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://")
    elif url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://")

    return url


# Create async engine
def _create_engine() -> AsyncEngine:
    """Create the async database engine."""
    settings = get_settings()
    url = _get_database_url()

    # Determine pool settings
    if "sqlite" in url:
        # SQLite doesn't support connection pool well
        poolclass = NullPool
    elif _is_test_environment():
        # Race condition fix: pytest-asyncio tạo event loop mới cho mỗi test.
        # Pool mặc định cache connection từ loop cũ → "Event loop is closed".
        # NullPool = tạo connection mới mỗi session, không pool → an toàn.
        poolclass = NullPool
        logger.info("Test environment detected — using NullPool")
    else:
        poolclass = None  # Default AsyncAdaptedQueuePool

    engine = create_async_engine(
        url,
        echo=settings.app_env == "development",
        poolclass=poolclass,
        pool_pre_ping=True,
    )

    logger.info(f"Database engine created: {url.split('@')[-1] if '@' in url else url}")
    return engine


def _is_test_environment() -> bool:
    """Phát hiện môi trường test.

    Returns True nếu đang chạy pytest (đặt bởi pytest_asyncio plugin
    thông qua biến PYTEST_CURRENT_TEST) hoặc APP_ENV=test.
    """
    # Cách 1: pytest tự set biến này
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return True
    # Cách 2: explicit env var
    if os.environ.get("APP_ENV") == "test":
        return True
    return False


# Global engine instance
_async_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Get or create the global engine instance."""
    global _async_engine
    if _async_engine is None:
        _async_engine = _create_engine()
    return _async_engine


# For backwards compatibility
@property  # type: ignore[misc]
def async_engine() -> AsyncEngine:
    """Get the async engine."""
    return get_engine()


# Session factory
_async_session_factory: AsyncSession | None = None


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = get_engine()
        _async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _async_session_factory


@property  # type: ignore[misc]
def async_session() -> async_sessionmaker[AsyncSession]:
    """Get the async session factory."""
    return get_session_factory()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to get a database session.

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_session)):
            ...
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for manual session management.

    Usage:
        async with get_session_context() as session:
            result = await session.execute(...)
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables() -> None:
    """Create all database tables.

    Call this on application startup.
    """
    from src.database.models import Base

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def drop_tables() -> None:
    """Drop all database tables.

    Use with caution - this is destructive!
    """
    from src.database.models import Base

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.warning("Database tables dropped")


async def close_engine() -> None:
    """Close the database engine.

    Call this on application shutdown.
    """
    global _async_engine, _async_session_factory
    if _async_engine is not None:
        await _async_engine.dispose()
        _async_engine = None
        _async_session_factory = None
        logger.info("Database engine closed")
