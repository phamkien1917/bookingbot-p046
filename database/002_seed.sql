-- Demo data for XHome VisitOps. Safe to run repeatedly after 001_schema.sql.

BEGIN;

-- Replace these placeholder hashes with real Argon2id hashes before enabling login.
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
    )
ON CONFLICT (id) DO NOTHING;

INSERT INTO customer_profiles (
    user_id, customer_code, preferred_contact_channel,
    budget_min, budget_max, marketing_consent
) VALUES (
    '10000000-0000-0000-0000-000000000001',
    'CUS-DEMO-001', 'IN_APP', 3000000000, 5500000000, FALSE
)
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO sale_profiles (
    user_id, employee_code, branch_name, job_title,
    specialties, max_daily_tours, calendar_provider,
    external_calendar_id, calendar_credentials_secret_ref
) VALUES (
    '10000000-0000-0000-0000-000000000002',
    'SALE-001', 'Trung tâm tư vấn Quận 1', 'Chuyên viên tư vấn',
    '["Căn hộ", "Đất nền khu Đông"]'::JSONB,
    6, 'GOOGLE', 'primary', 'secret://calendar/kien-sale'
)
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO vehicles (
    id, code, registration_number, display_name, seat_count
) VALUES (
    '20000000-0000-0000-0000-000000000001',
    'CAR-DEMO-01', '51A-123.45', 'Xe đưa đón 7 chỗ', 7
)
ON CONFLICT (id) DO NOTHING;

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
    id, property_id, media_type, url, caption, sort_order, is_cover
) VALUES
    (
        '50000000-0000-0000-0000-000000000001',
        '40000000-0000-0000-0000-000000000001',
        'IMAGE', 'https://images.example.com/sr-a1208-cover.jpg',
        'Ảnh đại diện căn A-1208', 0, TRUE
    ),
    (
        '50000000-0000-0000-0000-000000000002',
        '40000000-0000-0000-0000-000000000002',
        'IMAGE', 'https://images.example.com/sr-l18-cover.jpg',
        'Ảnh đại diện lô đất L18', 0, TRUE
    )
ON CONFLICT (id) DO NOTHING;

INSERT INTO property_sale_assignments (
    property_id, sale_user_id, is_primary, assigned_at
) VALUES
    (
        '40000000-0000-0000-0000-000000000001',
        '10000000-0000-0000-0000-000000000002', TRUE,
        '2026-01-01T00:00:00Z'
    ),
    (
        '40000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000002', TRUE,
        '2026-01-01T00:00:00Z'
    )
ON CONFLICT (property_id, sale_user_id) DO NOTHING;

INSERT INTO customer_preferences (
    id, customer_user_id, preference_key, preference_value,
    confidence, source, last_confirmed_at
) VALUES
    (
        '60000000-0000-0000-0000-000000000001',
        '10000000-0000-0000-0000-000000000001',
        'preferred_time_window',
        '{"days":["SAT","SUN"],"start":"13:00","end":"17:00"}'::JSONB,
        1, 'EXPLICIT', now()
    ),
    (
        '60000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000001',
        'needs_pickup', 'true'::JSONB, 1, 'EXPLICIT', now()
    )
ON CONFLICT (customer_user_id, preference_key) DO NOTHING;

INSERT INTO nearby_places (
    id, property_id, provider, provider_place_id, category,
    name, address, latitude, longitude, distance_m, travel_seconds, rating,
    expires_at
) VALUES (
    '70000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    'GOOGLE', 'demo-school-001', 'SCHOOL', 'Trường Quốc tế ABC',
    'Nhà Bè, TP. Hồ Chí Minh', 10.710000, 106.701000,
    1200, 300, 4.50, now() + INTERVAL '30 days'
)
ON CONFLICT (property_id, provider, provider_place_id) DO NOTHING;

COMMIT;
