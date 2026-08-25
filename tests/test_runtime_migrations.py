from src.database.migrations import POSTGRES_MIGRATIONS


def test_calendar_columns_have_idempotent_runtime_migrations() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS)
    for column in (
        "calendar_access_token",
        "calendar_refresh_token",
        "calendar_token_expires_at",
    ):
        assert f"ADD COLUMN IF NOT EXISTS {column}" in migration_sql


def test_runtime_migrations_never_delete_or_seed_business_data() -> None:
    migration_sql = "\n".join(POSTGRES_MIGRATIONS).upper()
    assert "DELETE FROM" not in migration_sql
    assert "INSERT INTO" not in migration_sql
