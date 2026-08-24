from src.database.migrations import POSTGRES_MIGRATIONS


def test_calendar_columns_have_idempotent_runtime_migrations() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS)
    for column in (
        "calendar_access_token",
        "calendar_refresh_token",
        "calendar_token_expires_at",
    ):
        assert f"ADD COLUMN IF NOT EXISTS {column}" in migration_sql
