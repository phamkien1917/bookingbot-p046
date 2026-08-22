"""Small idempotent migrations required before a full Alembic baseline exists."""

import logging

from sqlalchemy import text

from src.database.connection import get_engine

logger = logging.getLogger(__name__)


POSTGRES_MIGRATIONS = (
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_access_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_refresh_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_token_expires_at TIMESTAMPTZ",
    """
    UPDATE property_media
    SET url = 'https://www.nerahome.space/property-placeholder.svg'
    WHERE url IN (
        'https://images.example.com/sr-a1208-cover.jpg',
        'https://images.example.com/sr-l18-cover.jpg'
    )
    """,
)


async def apply_runtime_migrations() -> None:
    """Apply safe, repeatable PostgreSQL compatibility migrations."""
    engine = get_engine()
    if engine.dialect.name != "postgresql":
        logger.info("Skipping PostgreSQL runtime migrations for %s", engine.dialect.name)
        return

    async with engine.begin() as connection:
        for statement in POSTGRES_MIGRATIONS:
            await connection.execute(text(statement))
    logger.info("Runtime database migrations applied")
