"""Small idempotent migrations required before a full Alembic baseline exists."""

import logging

from sqlalchemy import text

from src.database.connection import get_engine

logger = logging.getLogger(__name__)


POSTGRES_MIGRATIONS = (
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_access_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_refresh_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_token_expires_at TIMESTAMPTZ",
    "ALTER TYPE notification_channel_t ADD VALUE IF NOT EXISTS 'ZALO'",
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_property_holds_one_active_property "
    "ON property_holds(property_id) WHERE status = 'ACTIVE'",
    "ALTER TABLE properties ADD COLUMN IF NOT EXISTS last_verified_at TIMESTAMPTZ",
    # Backfill once: a crawled listing was last known good when it was published.
    "UPDATE properties SET last_verified_at = published_at "
    "WHERE last_verified_at IS NULL AND published_at IS NOT NULL",
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
