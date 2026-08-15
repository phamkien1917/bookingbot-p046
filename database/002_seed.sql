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

INSERT INTO projects (
    id, code, name, developer_name, description, status,
    address_line, ward, district, province, latitude, longitude,
    default_hold_minutes, hold_warning_minutes, max_hold_extensions
) VALUES (
    '30000000-0000-0000-0000-000000000001',
    'SUNRISE-RIVERSIDE', 'Sunrise Riverside',
    'Doanh nghiệp Bất động sản X',
    'Dữ liệu dự án mẫu phục vụ demo đặt lịch xem nhà.',
    'ACTIVE', 'Đường Nguyễn Hữu Thọ', 'Phước Kiển', 'Nhà Bè',
    'TP. Hồ Chí Minh', 10.707900, 106.700400, 30, 5, 1
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO properties (
    id, project_id, code, property_kind, title, description, status,
    address_line, district, province, latitude, longitude,
    area_sqm, usable_area_sqm, bedrooms, bathrooms, floor_number,
    orientation, legal_status, list_price, features, published_at
) VALUES (
    '40000000-0000-0000-0000-000000000001',
    '30000000-0000-0000-0000-000000000001',
    'SR-A1208', 'APARTMENT', 'Căn hộ A-1208, 2 phòng ngủ',
    'Căn mẫu hướng sông dùng cho luồng demo.', 'AVAILABLE',
    'Đường Nguyễn Hữu Thọ', 'Nhà Bè', 'TP. Hồ Chí Minh',
    10.707900, 106.700400, 78.50, 72.00, 2, 2, 12,
    'ĐÔNG NAM', 'Hợp đồng mua bán', 4200000000,
    '{"balcony":true,"river_view":true,"parking":true}'::JSONB, now()
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO properties (
    id, project_id, code, property_kind, title, description, status,
    address_line, district, province, latitude, longitude,
    area_sqm, orientation, legal_status, list_price,
    parcel_number, map_sheet_number, land_use_purpose, land_use_term,
    frontage_m, road_width_m, features, published_at
) VALUES (
    '40000000-0000-0000-0000-000000000002',
    '30000000-0000-0000-0000-000000000001',
    'SR-L18', 'LAND', 'Lô đất L18, 100 m²',
    'Lô đất mẫu có hồ sơ pháp lý để demo tìm kiếm.', 'AVAILABLE',
    'Đường số 8', 'Nhà Bè', 'TP. Hồ Chí Minh',
    10.709100, 106.704500, 100.00, 'TÂY NAM',
    'Sổ hồng riêng', 5000000000, 'L18', '12',
    'Đất ở tại đô thị', 'Lâu dài', 5.00, 12.00,
    '{"near_park":true,"corner_lot":false}'::JSONB, now()
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO property_media (
    id, property_id, media_type, url, source, caption, sort_order, is_cover
) VALUES
    (
        '50000000-0000-0000-0000-000000000001',
        '40000000-0000-0000-0000-000000000001',
        'IMAGE', 'https://images.example.com/sr-a1208-cover.jpg',
        'DEMO', 'Ảnh đại diện căn A-1208', 0, TRUE
    ),
    (
        '50000000-0000-0000-0000-000000000002',
        '40000000-0000-0000-0000-000000000002',
        'IMAGE', 'https://images.example.com/sr-l18-cover.jpg',
        'DEMO', 'Ảnh đại diện lô đất L18', 0, TRUE
    )
ON CONFLICT (id) DO NOTHING;

INSERT INTO property_sale_assignments (
    property_id, sale_user_id, is_primary, assigned_at
) VALUES
    (
        '40000000-0000-0000-0000-000000000001',
        '10000000-0000-0000-0000-000000000002', TRUE, now()
    ),
    (
        '40000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000008', TRUE, now()
    )
ON CONFLICT (property_id, sale_user_id) DO NOTHING;

COMMIT;
