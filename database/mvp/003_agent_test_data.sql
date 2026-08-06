-- XHome MVP - synthetic dataset for testing the AI Agent
-- Run after database/mvp/001_schema.sql.
-- It is also safe to run after 002_seed.sql and safe to run repeatedly.
--
-- IMPORTANT: All names, projects, properties and prices below are synthetic.
-- Prices are plausible demo ranges only; they are not market quotations.

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Demo customer and coordinator accounts
-- ---------------------------------------------------------------------------

INSERT INTO users (
    id, role, email, phone, password_hash, full_name,
    status, email_verified_at, phone_verified_at
)
VALUES
    (
        '10000000-0000-0000-0000-000000000001',
        'CUSTOMER', 'customer.demo@example.com', '+84901234567',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Nguyễn Minh Anh',
        'ACTIVE', now(), now()
    ),
    (
        '10000000-0000-0000-0000-000000000003',
        'COORDINATOR', 'coordinator.demo@example.com', '+84921234567',
        'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH', 'Trần Điều Phối',
        'ACTIVE', now(), now()
    )
ON CONFLICT (id) DO UPDATE SET
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    full_name = EXCLUDED.full_name,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO customer_profiles (
    user_id,
    customer_code,
    preferred_contact_channel,
    budget_min,
    budget_max,
    desired_move_date,
    marketing_consent
)
VALUES (
    '10000000-0000-0000-0000-000000000001',
    'CUS-DEMO-001',
    'IN_APP',
    3000000000,
    7000000000,
    CURRENT_DATE + 90,
    FALSE
)
ON CONFLICT (user_id) DO UPDATE SET
    budget_min = EXCLUDED.budget_min,
    budget_max = EXCLUDED.budget_max,
    desired_move_date = EXCLUDED.desired_move_date,
    updated_at = now();

-- ---------------------------------------------------------------------------
-- 2. Ten demo sale accounts
-- ---------------------------------------------------------------------------

WITH sale_source(sale_no, full_name, specialty, branch_name) AS (
    VALUES
        (1,  'Nguyễn Minh Khang', 'Căn hộ',       'Chi nhánh Thủ Đức'),
        (2,  'Trần Ngọc Mai',     'Nhà phố',      'Chi nhánh Quận 7'),
        (3,  'Lê Hoàng Nam',      'Đất nền',      'Chi nhánh Nhà Bè'),
        (4,  'Phạm Thu Trang',    'Căn hộ',       'Chi nhánh Bình Chánh'),
        (5,  'Võ Quốc Bảo',       'Biệt thự',     'Chi nhánh Quận 7'),
        (6,  'Đặng Khánh Linh',   'Nhà liền kề',  'Chi nhánh Thủ Đức'),
        (7,  'Bùi Đức Anh',       'Đất nền',      'Chi nhánh Bình Chánh'),
        (8,  'Đỗ Thảo Vy',        'Thương mại',   'Chi nhánh Gò Vấp'),
        (9,  'Huỳnh Thành Đạt',   'Nhà phố',      'Chi nhánh Nhà Bè'),
        (10, 'Ngô Phương Thảo',   'Căn hộ',       'Chi nhánh Gò Vấp')
)
INSERT INTO users (
    id,
    role,
    email,
    phone,
    password_hash,
    full_name,
    status,
    email_verified_at,
    phone_verified_at
)
SELECT
    format('11000000-0000-0000-0000-%s', lpad(sale_no::TEXT, 12, '0'))::UUID,
    'SALE'::user_role_t,
    format('sale%s.demo@xhome.local', lpad(sale_no::TEXT, 2, '0'))::CITEXT,
    '+84970' || lpad(sale_no::TEXT, 6, '0'),
    'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH',
    full_name,
    'ACTIVE'::user_status_t,
    now(),
    now()
FROM sale_source
ON CONFLICT (id) DO UPDATE SET
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    full_name = EXCLUDED.full_name,
    status = EXCLUDED.status,
    updated_at = now();

WITH sale_source(sale_no, full_name, specialty, branch_name) AS (
    VALUES
        (1,  'Nguyễn Minh Khang', 'Căn hộ',       'Chi nhánh Thủ Đức'),
        (2,  'Trần Ngọc Mai',     'Nhà phố',      'Chi nhánh Quận 7'),
        (3,  'Lê Hoàng Nam',      'Đất nền',      'Chi nhánh Nhà Bè'),
        (4,  'Phạm Thu Trang',    'Căn hộ',       'Chi nhánh Bình Chánh'),
        (5,  'Võ Quốc Bảo',       'Biệt thự',     'Chi nhánh Quận 7'),
        (6,  'Đặng Khánh Linh',   'Nhà liền kề',  'Chi nhánh Thủ Đức'),
        (7,  'Bùi Đức Anh',       'Đất nền',      'Chi nhánh Bình Chánh'),
        (8,  'Đỗ Thảo Vy',        'Thương mại',   'Chi nhánh Gò Vấp'),
        (9,  'Huỳnh Thành Đạt',   'Nhà phố',      'Chi nhánh Nhà Bè'),
        (10, 'Ngô Phương Thảo',   'Căn hộ',       'Chi nhánh Gò Vấp')
)
INSERT INTO sale_profiles (
    user_id,
    employee_code,
    branch_name,
    job_title,
    specialties,
    max_daily_tours,
    is_accepting_tours
)
SELECT
    format('11000000-0000-0000-0000-%s', lpad(sale_no::TEXT, 12, '0'))::UUID,
    format('DEMO-SALE-%s', lpad(sale_no::TEXT, 2, '0')),
    branch_name,
    'Chuyên viên tư vấn bất động sản',
    jsonb_build_array(specialty, 'Tư vấn trực tiếp', 'Đặt lịch xem nhà'),
    5 + (sale_no % 4),
    TRUE
FROM sale_source
ON CONFLICT (user_id) DO UPDATE SET
    employee_code = EXCLUDED.employee_code,
    branch_name = EXCLUDED.branch_name,
    job_title = EXCLUDED.job_title,
    specialties = EXCLUDED.specialties,
    max_daily_tours = EXCLUDED.max_daily_tours,
    is_accepting_tours = TRUE,
    updated_at = now();

-- ---------------------------------------------------------------------------
-- 3. Five synthetic projects
-- ---------------------------------------------------------------------------

INSERT INTO projects (
    id,
    code,
    name,
    developer_name,
    description,
    status,
    address_line,
    ward,
    district,
    province,
    latitude,
    longitude,
    default_hold_minutes,
    hold_warning_minutes,
    max_hold_extensions,
    metadata
)
VALUES
    (
        '31000000-0000-0000-0000-000000000001',
        'DEMO-METRO-EAST', 'Metro East Residence', 'XHome Demo',
        'Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.',
        'ACTIVE', 'Đường Nguyễn Xiển', 'Long Thạnh Mỹ', 'Thủ Đức',
        'TP. Hồ Chí Minh', 10.842400, 106.835100, 30, 5, 1,
        '{"demo_data":true,"segment":"mid_range"}'::JSONB
    ),
    (
        '31000000-0000-0000-0000-000000000002',
        'DEMO-SOUTH-GARDEN', 'South Garden Residence', 'XHome Demo',
        'Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.',
        'ACTIVE', 'Đường Nguyễn Hữu Thọ', 'Tân Phong', 'Quận 7',
        'TP. Hồ Chí Minh', 10.729400, 106.703300, 30, 5, 1,
        '{"demo_data":true,"segment":"upper_mid"}'::JSONB
    ),
    (
        '31000000-0000-0000-0000-000000000003',
        'DEMO-RIVERSIDE-NB', 'Nhà Bè Riverside', 'XHome Demo',
        'Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.',
        'ACTIVE', 'Đường Lê Văn Lương', 'Phước Kiển', 'Nhà Bè',
        'TP. Hồ Chí Minh', 10.704000, 106.702000, 45, 10, 1,
        '{"demo_data":true,"segment":"mixed"}'::JSONB
    ),
    (
        '31000000-0000-0000-0000-000000000004',
        'DEMO-WEST-GATE', 'West Gate Town', 'XHome Demo',
        'Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.',
        'ACTIVE', 'Đường Nguyễn Văn Linh', 'An Phú Tây', 'Bình Chánh',
        'TP. Hồ Chí Minh', 10.681900, 106.609700, 60, 10, 2,
        '{"demo_data":true,"segment":"affordable"}'::JSONB
    ),
    (
        '31000000-0000-0000-0000-000000000005',
        'DEMO-NORTH-PARK', 'North Park Homes', 'XHome Demo',
        'Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.',
        'ACTIVE', 'Đường Phan Văn Trị', 'Phường 5', 'Gò Vấp',
        'TP. Hồ Chí Minh', 10.827500, 106.688600, 30, 5, 1,
        '{"demo_data":true,"segment":"urban"}'::JSONB
    )
ON CONFLICT (id) DO UPDATE SET
    code = EXCLUDED.code,
    name = EXCLUDED.name,
    developer_name = EXCLUDED.developer_name,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    address_line = EXCLUDED.address_line,
    ward = EXCLUDED.ward,
    district = EXCLUDED.district,
    province = EXCLUDED.province,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    default_hold_minutes = EXCLUDED.default_hold_minutes,
    hold_warning_minutes = EXCLUDED.hold_warning_minutes,
    max_hold_extensions = EXCLUDED.max_hold_extensions,
    metadata = EXCLUDED.metadata,
    updated_at = now();

-- ---------------------------------------------------------------------------
-- 4. Sixty synthetic properties with varied searchable attributes
-- ---------------------------------------------------------------------------

WITH base AS (
    SELECT
        i,
        ((i - 1) % 5) + 1 AS project_no,
        CASE ((i - 1) % 6)
            WHEN 0 THEN 'APARTMENT'
            WHEN 1 THEN 'HOUSE'
            WHEN 2 THEN 'LAND'
            WHEN 3 THEN 'TOWNHOUSE'
            WHEN 4 THEN 'VILLA'
            ELSE 'COMMERCIAL'
        END AS kind
    FROM generate_series(1, 60) AS g(i)
),
calculated AS (
    SELECT
        *,
        CASE kind
            WHEN 'APARTMENT' THEN (48 + (i % 7) * 9)::NUMERIC(12, 2)
            WHEN 'HOUSE' THEN (62 + (i % 8) * 14)::NUMERIC(12, 2)
            WHEN 'LAND' THEN (80 + (i % 9) * 20)::NUMERIC(12, 2)
            WHEN 'TOWNHOUSE' THEN (75 + (i % 7) * 15)::NUMERIC(12, 2)
            WHEN 'VILLA' THEN (160 + (i % 8) * 35)::NUMERIC(12, 2)
            ELSE (70 + (i % 8) * 18)::NUMERIC(12, 2)
        END AS area_value
    FROM base
)
INSERT INTO properties (
    id,
    project_id,
    code,
    property_kind,
    title,
    description,
    status,
    address_line,
    ward,
    district,
    province,
    latitude,
    longitude,
    area_sqm,
    usable_area_sqm,
    bedrooms,
    bathrooms,
    floor_number,
    orientation,
    legal_status,
    list_price,
    currency,
    parcel_number,
    map_sheet_number,
    land_use_purpose,
    land_use_term,
    frontage_m,
    road_width_m,
    features,
    published_at
)
SELECT
    format('41000000-0000-0000-0000-%s', lpad(i::TEXT, 12, '0'))::UUID,
    format('31000000-0000-0000-0000-%s', lpad(project_no::TEXT, 12, '0'))::UUID,
    format(
        'DEMO-%s-%s',
        CASE kind
            WHEN 'APARTMENT' THEN 'APT'
            WHEN 'HOUSE' THEN 'HOU'
            WHEN 'LAND' THEN 'LAN'
            WHEN 'TOWNHOUSE' THEN 'TOW'
            WHEN 'VILLA' THEN 'VIL'
            ELSE 'COM'
        END,
        lpad(i::TEXT, 3, '0')
    ),
    kind::property_kind_t,
    CASE kind
        WHEN 'APARTMENT' THEN format('Căn hộ demo %s - %s phòng ngủ', lpad(i::TEXT, 3, '0'), 1 + (i % 3))
        WHEN 'HOUSE' THEN format('Nhà phố demo %s - khu dân cư hiện hữu', lpad(i::TEXT, 3, '0'))
        WHEN 'LAND' THEN format('Lô đất demo %s - pháp lý riêng', lpad(i::TEXT, 3, '0'))
        WHEN 'TOWNHOUSE' THEN format('Nhà liền kề demo %s - mặt tiền nội khu', lpad(i::TEXT, 3, '0'))
        WHEN 'VILLA' THEN format('Biệt thự demo %s - không gian sân vườn', lpad(i::TEXT, 3, '0'))
        ELSE format('Mặt bằng thương mại demo %s', lpad(i::TEXT, 3, '0'))
    END,
    format(
        'Dữ liệu tổng hợp để kiểm thử AI Agent. Loại %s, diện tích %s m², thuộc khu vực %s.',
        kind,
        area_value,
        CASE project_no
            WHEN 1 THEN 'Thủ Đức'
            WHEN 2 THEN 'Quận 7'
            WHEN 3 THEN 'Nhà Bè'
            WHEN 4 THEN 'Bình Chánh'
            ELSE 'Gò Vấp'
        END
    ),
    CASE
        WHEN i % 23 = 0 THEN 'MAINTENANCE'
        WHEN i % 17 = 0 THEN 'SOLD'
        WHEN i % 11 = 0 THEN 'UNDER_OFFER'
        ELSE 'AVAILABLE'
    END::property_status_t,
    CASE project_no
        WHEN 1 THEN format('Đường Nguyễn Xiển, căn/lô %s', lpad(i::TEXT, 3, '0'))
        WHEN 2 THEN format('Đường Nguyễn Hữu Thọ, căn/lô %s', lpad(i::TEXT, 3, '0'))
        WHEN 3 THEN format('Đường Lê Văn Lương, căn/lô %s', lpad(i::TEXT, 3, '0'))
        WHEN 4 THEN format('Đường Nguyễn Văn Linh, căn/lô %s', lpad(i::TEXT, 3, '0'))
        ELSE format('Đường Phan Văn Trị, căn/lô %s', lpad(i::TEXT, 3, '0'))
    END,
    CASE project_no
        WHEN 1 THEN 'Long Thạnh Mỹ'
        WHEN 2 THEN 'Tân Phong'
        WHEN 3 THEN 'Phước Kiển'
        WHEN 4 THEN 'An Phú Tây'
        ELSE 'Phường 5'
    END,
    CASE project_no
        WHEN 1 THEN 'Thủ Đức'
        WHEN 2 THEN 'Quận 7'
        WHEN 3 THEN 'Nhà Bè'
        WHEN 4 THEN 'Bình Chánh'
        ELSE 'Gò Vấp'
    END,
    'TP. Hồ Chí Minh',
    CASE project_no
        WHEN 1 THEN 10.842400
        WHEN 2 THEN 10.729400
        WHEN 3 THEN 10.704000
        WHEN 4 THEN 10.681900
        ELSE 10.827500
    END + ((i % 7) * 0.000250),
    CASE project_no
        WHEN 1 THEN 106.835100
        WHEN 2 THEN 106.703300
        WHEN 3 THEN 106.702000
        WHEN 4 THEN 106.609700
        ELSE 106.688600
    END + ((i % 5) * 0.000300),
    area_value,
    CASE WHEN kind = 'LAND' THEN NULL ELSE round(area_value * 0.88, 2) END,
    CASE kind
        WHEN 'APARTMENT' THEN 1 + (i % 3)
        WHEN 'HOUSE' THEN 2 + (i % 4)
        WHEN 'TOWNHOUSE' THEN 3 + (i % 3)
        WHEN 'VILLA' THEN 4 + (i % 4)
        ELSE NULL
    END::SMALLINT,
    CASE kind
        WHEN 'APARTMENT' THEN 1 + (i % 2)
        WHEN 'HOUSE' THEN 2 + (i % 3)
        WHEN 'TOWNHOUSE' THEN 2 + (i % 3)
        WHEN 'VILLA' THEN 3 + (i % 3)
        ELSE NULL
    END::SMALLINT,
    CASE
        WHEN kind IN ('APARTMENT', 'COMMERCIAL') THEN 2 + (i % 22)
        ELSE NULL
    END::SMALLINT,
    (ARRAY['ĐÔNG', 'TÂY', 'NAM', 'BẮC', 'ĐÔNG NAM', 'TÂY NAM'])[(i % 6) + 1],
    CASE
        WHEN kind = 'LAND' THEN 'Sổ đỏ riêng - dữ liệu demo'
        ELSE 'Sổ hồng/Hợp đồng mua bán - dữ liệu demo'
    END,
    CASE kind
        WHEN 'APARTMENT' THEN 2200000000::NUMERIC + (i % 9) * 450000000::NUMERIC
        WHEN 'HOUSE' THEN 4800000000::NUMERIC + (i % 10) * 720000000::NUMERIC
        WHEN 'LAND' THEN 2800000000::NUMERIC + (i % 10) * 650000000::NUMERIC
        WHEN 'TOWNHOUSE' THEN 6800000000::NUMERIC + (i % 9) * 950000000::NUMERIC
        WHEN 'VILLA' THEN 13500000000::NUMERIC + (i % 8) * 2800000000::NUMERIC
        ELSE 8500000000::NUMERIC + (i % 9) * 1600000000::NUMERIC
    END,
    'VND',
    CASE WHEN kind = 'LAND' THEN format('DEMO-PARCEL-%s', lpad(i::TEXT, 3, '0')) ELSE NULL END,
    CASE WHEN kind = 'LAND' THEN format('DEMO-MAP-%s', lpad(project_no::TEXT, 2, '0')) ELSE NULL END,
    CASE WHEN kind = 'LAND' THEN 'Đất ở tại đô thị' ELSE NULL END,
    CASE WHEN kind = 'LAND' THEN 'Lâu dài' ELSE NULL END,
    CASE
        WHEN kind IN ('HOUSE', 'LAND', 'TOWNHOUSE', 'VILLA')
        THEN (4 + (i % 6) * 0.5)::NUMERIC(10, 2)
        ELSE NULL
    END,
    CASE
        WHEN kind IN ('HOUSE', 'LAND', 'TOWNHOUSE', 'VILLA', 'COMMERCIAL')
        THEN (6 + (i % 5) * 2)::NUMERIC(10, 2)
        ELSE NULL
    END,
    jsonb_build_object(
        'demo_data', TRUE,
        'near_school', i % 2 = 0,
        'near_hospital', i % 3 = 0,
        'near_market', i % 4 <> 0,
        'parking', kind <> 'LAND',
        'balcony', kind = 'APARTMENT',
        'elevator', kind IN ('APARTMENT', 'COMMERCIAL'),
        'river_view', project_no IN (2, 3) AND i % 2 = 0,
        'pool', kind IN ('APARTMENT', 'VILLA') AND i % 3 = 0,
        'gym', kind = 'APARTMENT' AND i % 2 = 1,
        'distance_to_center_km', 5 + (i % 16)
    ),
    now() - make_interval(days => i % 45)
FROM calculated
ON CONFLICT (id) DO UPDATE SET
    project_id = EXCLUDED.project_id,
    code = EXCLUDED.code,
    property_kind = EXCLUDED.property_kind,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    address_line = EXCLUDED.address_line,
    ward = EXCLUDED.ward,
    district = EXCLUDED.district,
    province = EXCLUDED.province,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    area_sqm = EXCLUDED.area_sqm,
    usable_area_sqm = EXCLUDED.usable_area_sqm,
    bedrooms = EXCLUDED.bedrooms,
    bathrooms = EXCLUDED.bathrooms,
    floor_number = EXCLUDED.floor_number,
    orientation = EXCLUDED.orientation,
    legal_status = EXCLUDED.legal_status,
    list_price = EXCLUDED.list_price,
    currency = EXCLUDED.currency,
    parcel_number = EXCLUDED.parcel_number,
    map_sheet_number = EXCLUDED.map_sheet_number,
    land_use_purpose = EXCLUDED.land_use_purpose,
    land_use_term = EXCLUDED.land_use_term,
    frontage_m = EXCLUDED.frontage_m,
    road_width_m = EXCLUDED.road_width_m,
    features = EXCLUDED.features,
    published_at = EXCLUDED.published_at,
    updated_at = now();

-- ---------------------------------------------------------------------------
-- 5. Assign every generated property to one primary sale
-- ---------------------------------------------------------------------------

WITH ranked_properties AS (
    SELECT
        id AS property_id,
        row_number() OVER (ORDER BY code) AS property_no
    FROM properties
    WHERE code LIKE 'DEMO-%'
      AND id::TEXT LIKE '41000000-%'
)
INSERT INTO property_sale_assignments (
    property_id,
    sale_user_id,
    is_primary,
    assigned_at
)
SELECT
    property_id,
    format(
        '11000000-0000-0000-0000-%s',
        lpad((((property_no - 1) % 10) + 1)::TEXT, 12, '0')
    )::UUID,
    TRUE,
    now()
FROM ranked_properties
ON CONFLICT (property_id, sale_user_id) DO UPDATE SET
    is_primary = TRUE,
    unassigned_at = NULL;

-- ---------------------------------------------------------------------------
-- 6. Twenty busy time ranges: two for each demo sale
-- ---------------------------------------------------------------------------

WITH busy_slots(slot_no, days_ahead, start_time, end_time, reason) AS (
    VALUES
        (1, 1, TIME '09:00', TIME '10:30', 'Họp nội bộ - dữ liệu demo'),
        (2, 2, TIME '14:00', TIME '16:00', 'Đang dẫn khách - dữ liệu demo')
),
sale_numbers AS (
    SELECT generate_series(1, 10) AS sale_no
)
INSERT INTO sale_unavailability (
    id,
    sale_user_id,
    unavailable_during,
    reason,
    source,
    external_reference
)
SELECT
    format(
        '13000000-0000-0000-0000-%s',
        lpad((((sale_no - 1) * 2) + slot_no)::TEXT, 12, '0')
    )::UUID,
    format('11000000-0000-0000-0000-%s', lpad(sale_no::TEXT, 12, '0'))::UUID,
    tstzrange(
        ((CURRENT_DATE + days_ahead) + start_time) AT TIME ZONE 'Asia/Ho_Chi_Minh',
        ((CURRENT_DATE + days_ahead) + end_time) AT TIME ZONE 'Asia/Ho_Chi_Minh',
        '[)'
    ),
    reason,
    'SYSTEM',
    format('DEMO-BUSY-%s-%s', lpad(sale_no::TEXT, 2, '0'), slot_no)
FROM sale_numbers
CROSS JOIN busy_slots
ON CONFLICT (id) DO UPDATE SET
    sale_user_id = EXCLUDED.sale_user_id,
    unavailable_during = EXCLUDED.unavailable_during,
    reason = EXCLUDED.reason,
    source = EXCLUDED.source,
    external_reference = EXCLUDED.external_reference;

COMMIT;

-- ---------------------------------------------------------------------------
-- 7. Verification results shown after a successful run
-- ---------------------------------------------------------------------------

SELECT 'demo_sales' AS metric, count(*)::TEXT AS value
FROM sale_profiles
WHERE employee_code LIKE 'DEMO-SALE-%'
UNION ALL
SELECT 'demo_projects', count(*)::TEXT
FROM projects
WHERE code LIKE 'DEMO-%'
UNION ALL
SELECT 'demo_properties', count(*)::TEXT
FROM properties
WHERE id::TEXT LIKE '41000000-%'
UNION ALL
SELECT 'demo_assignments', count(*)::TEXT
FROM property_sale_assignments psa
JOIN properties p ON p.id = psa.property_id
WHERE p.id::TEXT LIKE '41000000-%'
UNION ALL
SELECT 'demo_busy_slots', count(*)::TEXT
FROM sale_unavailability
WHERE external_reference LIKE 'DEMO-BUSY-%';

SELECT
    property_kind,
    status,
    count(*) AS property_count,
    min(list_price) AS minimum_price,
    max(list_price) AS maximum_price
FROM properties
WHERE id::TEXT LIKE '41000000-%'
GROUP BY property_kind, status
ORDER BY property_kind, status;
