-- Demo data for the 18-table XHome VisitOps MVP schema.
-- Safe to run repeatedly after database/001_schema.sql.

BEGIN;

-- Replace these placeholder values with real Argon2id hashes before enabling login.
INSERT INTO users (
    id, role, email, phone, password_hash, full_name,
    email_verified_at, phone_verified_at
) VALUES
    (
        '10000000-0000-0000-0000-000000000001',
        'CUSTOMER', 'customer.demo@example.com', '+84901234567',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Nguyễn Minh Anh', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000002',
        'SALE', 'kien.sale@example.com', '+84911234567',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Phạm Kiên', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000003',
        'COORDINATOR', 'coordinator.demo@example.com', '+84921234567',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trần Điều Phối', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000004',
        'CUSTOMER', 'thuha.customer.demo@example.com', '+84900000004',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Lê Thu Hà', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000005',
        'CUSTOMER', 'hoangnam.customer.demo@example.com', '+84900000005',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trần Hoàng Nam', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000006',
        'CUSTOMER', 'ngoclan.customer.demo@example.com', '+84900000006',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Vũ Ngọc Lan', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000007',
        'CUSTOMER', 'giahuy.customer.demo@example.com', '+84900000007',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Đỗ Gia Huy', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000008',
        'SALE', 'minhquan.sale.demo@example.com', '+84900000008',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trần Minh Quân', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000009',
        'SALE', 'thutrang.sale.demo@example.com', '+84900000009',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Nguyễn Thu Trang', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000010',
        'ADMIN', 'admin.demo@example.com', '+84900000010',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Nguyễn Quản Trị', now(), now()
    )
ON CONFLICT (id) DO NOTHING;

INSERT INTO customer_profiles (
    user_id, customer_code, preferred_contact_channel,
    budget_min, budget_max, marketing_consent
) VALUES
    (
        '10000000-0000-0000-0000-000000000001',
        'CUS-DEMO-001', 'IN_APP', 3000000000, 5500000000, FALSE
    ),
    (
        '10000000-0000-0000-0000-000000000004',
        'CUS-DEMO-002', 'EMAIL', 2000000000, 4000000000, FALSE
    ),
    (
        '10000000-0000-0000-0000-000000000005',
        'CUS-DEMO-003', 'IN_APP', 4500000000, 7500000000, FALSE
    ),
    (
        '10000000-0000-0000-0000-000000000006',
        'CUS-DEMO-004', 'SMS', 1500000000, 3000000000, TRUE
    ),
    (
        '10000000-0000-0000-0000-000000000007',
        'CUS-DEMO-005', 'IN_APP', 6000000000, 10000000000, FALSE
    )
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO sale_profiles (
    user_id, employee_code, branch_name, job_title,
    specialties, max_daily_tours, calendar_provider,
    external_calendar_id, calendar_credentials_secret_ref
) VALUES
    (
        '10000000-0000-0000-0000-000000000002',
        'SALE-001', 'Trung tâm tư vấn Quận 1', 'Chuyên viên tư vấn',
        '["Căn hộ", "Đất nền khu Đông"]'::JSONB,
        6, 'GOOGLE', 'primary', 'secret://calendar/kien-sale'
    ),
    (
        '10000000-0000-0000-0000-000000000008',
        'SALE-002', 'Trung tâm tư vấn Hà Nội', 'Chuyên viên tư vấn',
        '["Nhà phố", "Đất nền", "Biệt thự"]'::JSONB,
        7, 'OUTLOOK', 'minhquan-primary', 'secret://calendar/minhquan-sale'
    ),
    (
        '10000000-0000-0000-0000-000000000009',
        'SALE-003', 'Trung tâm tư vấn TP. Hồ Chí Minh', 'Chuyên viên tư vấn cao cấp',
        '["Căn hộ", "Nhà riêng", "Bất động sản thương mại"]'::JSONB,
        8, 'GOOGLE', 'thutrang-primary', 'secret://calendar/thutrang-sale'
    )
ON CONFLICT (user_id) DO NOTHING;

COMMIT;
