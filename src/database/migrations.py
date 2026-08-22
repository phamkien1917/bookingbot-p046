"""Small idempotent migrations required before a full Alembic baseline exists."""

import logging

from sqlalchemy import text

from src.database.connection import get_engine

logger = logging.getLogger(__name__)


POSTGRES_MIGRATIONS = (
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_access_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_refresh_token TEXT",
    "ALTER TABLE sale_profiles ADD COLUMN IF NOT EXISTS calendar_token_expires_at TIMESTAMPTZ",
    "DELETE FROM property_media WHERE property_id IN (SELECT id FROM properties WHERE code IN ('SR-A1208', 'SR-L18'))",
    "DELETE FROM property_sale_assignments WHERE property_id IN (SELECT id FROM properties WHERE code IN ('SR-A1208', 'SR-L18'))",
    "DELETE FROM properties WHERE code IN ('SR-A1208', 'SR-L18')",
    """
    INSERT INTO users (id, role, email, phone, password_hash, full_name, email_verified_at, phone_verified_at) VALUES
    ('20000000-0000-0000-0000-000000000000', 'SALE', 'hanh.bt.sale0@xhome.com', '+84999000000', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Bùi Thị Hạnh', now(), now()),
    ('20000000-0000-0000-0000-000000000001', 'SALE', 'tuan.dv.sale1@xhome.com', '+84999000001', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đào Văn Tuân', now(), now()),
    ('20000000-0000-0000-0000-000000000002', 'SALE', 'yen.mt.sale2@xhome.com', '+84999000002', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Mai Thị Yến', now(), now()),
    ('20000000-0000-0000-0000-000000000003', 'SALE', 'mai.dt.sale3@xhome.com', '+84999000003', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Dương Thị Mai', now(), now()),
    ('20000000-0000-0000-0000-000000000004', 'SALE', 'kim.ht.sale4@xhome.com', '+84999000004', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Hồ Thị Kim', now(), now()),
    ('20000000-0000-0000-0000-000000000005', 'SALE', 'hoa.vt.sale5@xhome.com', '+84999000005', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Vũ Thị Hoa', now(), now()),
    ('20000000-0000-0000-0000-000000000006', 'SALE', 'quynh.lt.sale6@xhome.com', '+84999000006', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Lâm Thị Quỳnh', now(), now()),
    ('20000000-0000-0000-0000-000000000007', 'SALE', 'cong.lh.sale7@xhome.com', '+84999000007', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Lý Hoàng Công', now(), now()),
    ('20000000-0000-0000-0000-000000000008', 'SALE', 'oanh.dt.sale8@xhome.com', '+84999000008', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đinh Thị Oanh', now(), now()),
    ('20000000-0000-0000-0000-000000000009', 'SALE', 'nam.lv.sale9@xhome.com', '+84999000009', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Lê Văn Nam', now(), now()),
    ('20000000-0000-0000-0000-000000000010', 'SALE', 'an.nv.sale10@xhome.com', '+84999000010', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Nguyễn Văn An', now(), now()),
    ('20000000-0000-0000-0000-000000000011', 'SALE', 'bich.tt.sale11@xhome.com', '+84999000011', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trần Thị Bích', now(), now()),
    ('20000000-0000-0000-0000-000000000012', 'SALE', 'lam.nv.sale12@xhome.com', '+84999000012', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Ngô Văn Lâm', now(), now()),
    ('20000000-0000-0000-0000-000000000013', 'SALE', 'xuan.pt.sale13@xhome.com', '+84999000013', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Phan Thị Xuân', now(), now()),
    ('20000000-0000-0000-0000-000000000014', 'SALE', 'phong.dv.sale14@xhome.com', '+84999000014', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đoàn Văn Phong', now(), now()),
    ('20000000-0000-0000-0000-000000000015', 'SALE', 'giang.dv.sale15@xhome.com', '+84999000015', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đặng Văn Giang', now(), now()),
    ('20000000-0000-0000-0000-000000000016', 'SALE', 'dung.pt.sale16@xhome.com', '+84999000016', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Phạm Thị Dung', now(), now()),
    ('20000000-0000-0000-0000-000000000017', 'SALE', 'an.hv.sale17@xhome.com', '+84999000017', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Hoàng Văn Ân', now(), now()),
    ('20000000-0000-0000-0000-000000000018', 'SALE', 'inh.dv.sale18@xhome.com', '+84999000018', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đỗ Văn Inh', now(), now()),
    ('20000000-0000-0000-0000-000000000019', 'SALE', 'quan.tv.sale19@xhome.com', '+84999000019', 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trịnh Văn Quân', now(), now())
    ON CONFLICT (email) DO NOTHING
    """,
    """
    INSERT INTO sale_profiles (user_id, employee_code, branch_name, job_title, specialties, max_daily_tours, calendar_provider)
    SELECT id, 'NV-' || SUBSTRING(id::text, 33, 4), 'Văn phòng kinh doanh', 'Chuyên viên tư vấn', '["Căn hộ", "Nhà phố"]'::JSONB, 8, 'GOOGLE'
    FROM users WHERE email LIKE '%@xhome.com'
    ON CONFLICT (user_id) DO NOTHING
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
