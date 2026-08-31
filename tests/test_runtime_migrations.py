from src.database.migrations import POSTGRES_MIGRATIONS


def test_calendar_columns_have_idempotent_runtime_migrations() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS)
    for column in (
        "calendar_access_token",
        "calendar_refresh_token",
        "calendar_token_expires_at",
    ):
        assert f"ADD COLUMN IF NOT EXISTS {column}" in migration_sql


def test_listing_freshness_column_has_idempotent_runtime_migration() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS)
    assert "ADD COLUMN IF NOT EXISTS last_verified_at" in migration_sql
    # The backfill must never overwrite a verification a sale already recorded.
    assert "WHERE last_verified_at IS NULL AND published_at IS NOT NULL" in migration_sql


def test_runtime_migrations_never_delete_or_seed_business_data() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS).upper()
    assert "DELETE FROM" not in migration_sql
    assert "INSERT INTO" not in migration_sql
