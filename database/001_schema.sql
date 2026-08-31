-- XHome VisitOps - PostgreSQL schema for the MVP
-- Scope: AI consultation -> property selection -> sale approval -> appointment -> soft hold.
-- Contains 18 business tables: the original 16-table MVP plus normalized
-- external seller data for crawled listings. Run on an empty PostgreSQL/Neon database.
-- Advanced modules such as vehicles, route optimization, nearby places,
-- customer memory, automatic rescheduling, analytics and audit logs are not included.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- ---------------------------------------------------------------------------
-- Shared types
-- ---------------------------------------------------------------------------

CREATE TYPE user_role_t AS ENUM ('CUSTOMER', 'SALE', 'COORDINATOR', 'ADMIN');
CREATE TYPE user_status_t AS ENUM ('ACTIVE', 'LOCKED', 'DISABLED');
CREATE TYPE property_kind_t AS ENUM (
    'LAND', 'APARTMENT', 'HOUSE', 'VILLA', 'TOWNHOUSE', 'COMMERCIAL'
);
CREATE TYPE property_status_t AS ENUM (
    'DRAFT', 'AVAILABLE', 'UNDER_OFFER', 'SOLD', 'HIDDEN', 'MAINTENANCE'
);
CREATE TYPE tour_mode_t AS ENUM ('IN_PERSON', 'VIDEO');
CREATE TYPE request_status_t AS ENUM (
    'DRAFT', 'COLLECTING', 'OPTIONS_PROPOSED', 'WAITING_APPROVAL',
    'APPROVED', 'REJECTED', 'EXPIRED', 'CANCELLED', 'BOOKED'
);
CREATE TYPE slot_status_t AS ENUM ('PROPOSED', 'SELECTED', 'EXPIRED', 'WITHDRAWN');
CREATE TYPE approval_status_t AS ENUM (
    'PENDING', 'APPROVED', 'REJECTED', 'EXPIRED', 'CANCELLED'
);
CREATE TYPE appointment_status_t AS ENUM (
    'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'NO_SHOW', 'RESCHEDULED', 'CANCELLED'
);
CREATE TYPE hold_status_t AS ENUM ('ACTIVE', 'EXPIRED', 'RELEASED', 'CONVERTED');
CREATE TYPE message_role_t AS ENUM ('USER', 'ASSISTANT', 'TOOL', 'SYSTEM');
CREATE TYPE notification_channel_t AS ENUM ('IN_APP', 'EMAIL', 'SMS', 'WEB_PUSH');
CREATE TYPE delivery_status_t AS ENUM ('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'CANCELLED');
CREATE TYPE sync_status_t AS ENUM ('NOT_REQUESTED', 'PENDING', 'SYNCED', 'FAILED');

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- ---------------------------------------------------------------------------
-- 1-3. Users and role-specific profiles
-- ---------------------------------------------------------------------------

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role user_role_t NOT NULL,
    email CITEXT NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash TEXT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    avatar_url TEXT,
    status user_status_t NOT NULL DEFAULT 'ACTIVE',
    timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Ho_Chi_Minh',
    locale VARCHAR(16) NOT NULL DEFAULT 'vi-VN',
    email_verified_at TIMESTAMPTZ,
    phone_verified_at TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT user_email_not_blank CHECK (length(trim(email::TEXT)) > 0),
    CONSTRAINT user_phone_normalized CHECK (phone IS NULL OR phone ~ '^\+?[0-9]{8,15}$')
);

CREATE UNIQUE INDEX uq_users_phone ON users(phone) WHERE phone IS NOT NULL;

CREATE TABLE customer_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    customer_code VARCHAR(32) NOT NULL UNIQUE,
    identity_verified_at TIMESTAMPTZ,
    preferred_contact_channel notification_channel_t NOT NULL DEFAULT 'IN_APP',
    budget_min NUMERIC(18, 2),
    budget_max NUMERIC(18, 2),
    desired_move_date DATE,
    marketing_consent BOOLEAN NOT NULL DEFAULT FALSE,
    internal_note TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT customer_budget_non_negative CHECK (
        (budget_min IS NULL OR budget_min >= 0)
        AND (budget_max IS NULL OR budget_max >= 0)
    ),
    CONSTRAINT customer_budget_valid CHECK (
        budget_min IS NULL OR budget_max IS NULL OR budget_min <= budget_max
    )
);

CREATE TABLE sale_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    employee_code VARCHAR(32) NOT NULL UNIQUE,
    branch_name VARCHAR(150),
    job_title VARCHAR(100),
    specialties JSONB NOT NULL DEFAULT '[]'::JSONB,
    working_hours JSONB NOT NULL DEFAULT
        '{"mon":["08:00","18:00"],"tue":["08:00","18:00"],"wed":["08:00","18:00"],"thu":["08:00","18:00"],"fri":["08:00","18:00"],"sat":["08:00","18:00"]}'::JSONB,
    max_daily_tours SMALLINT NOT NULL DEFAULT 8,
    is_accepting_tours BOOLEAN NOT NULL DEFAULT TRUE,
    calendar_provider VARCHAR(20),
    external_calendar_id TEXT,
    calendar_credentials_secret_ref TEXT,
    calendar_access_token TEXT,
    calendar_refresh_token TEXT,
    calendar_token_expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT sale_daily_limit_positive CHECK (max_daily_tours > 0),
    CONSTRAINT sale_calendar_provider_valid CHECK (
        calendar_provider IS NULL OR calendar_provider IN ('GOOGLE', 'OUTLOOK')
    )
);

CREATE OR REPLACE FUNCTION assert_profile_role()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    actual_role user_role_t;
    expected_role user_role_t := TG_ARGV[0]::user_role_t;
BEGIN
    SELECT role INTO actual_role FROM users WHERE id = NEW.user_id;
    IF actual_role IS DISTINCT FROM expected_role THEN
        RAISE EXCEPTION 'User % must have role %, actual role is %',
            NEW.user_id, expected_role, actual_role;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_customer_profile_role
BEFORE INSERT OR UPDATE OF user_id ON customer_profiles
FOR EACH ROW EXECUTE FUNCTION assert_profile_role('CUSTOMER');

CREATE TRIGGER trg_sale_profile_role
BEFORE INSERT OR UPDATE OF user_id ON sale_profiles
FOR EACH ROW EXECUTE FUNCTION assert_profile_role('SALE');

-- ---------------------------------------------------------------------------
-- 4-10. Property inventory, external sellers and sale availability
-- ---------------------------------------------------------------------------

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(32) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    developer_name VARCHAR(200),
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    address_line TEXT NOT NULL,
    ward VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100) NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    default_hold_minutes SMALLINT NOT NULL DEFAULT 30,
    hold_warning_minutes SMALLINT NOT NULL DEFAULT 5,
    max_hold_extensions SMALLINT NOT NULL DEFAULT 1,
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT project_status_valid CHECK (
        status IN ('DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED')
    ),
    CONSTRAINT project_geo_valid CHECK (
        (latitude IS NULL OR latitude BETWEEN -90 AND 90)
        AND (longitude IS NULL OR longitude BETWEEN -180 AND 180)
    ),
    CONSTRAINT project_hold_policy_valid CHECK (
        default_hold_minutes > 0
        AND hold_warning_minutes >= 0
        AND hold_warning_minutes < default_hold_minutes
        AND max_hold_extensions >= 0
    )
);

CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    property_kind property_kind_t NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status property_status_t NOT NULL DEFAULT 'DRAFT',
    address_line TEXT,
    ward VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    area_sqm NUMERIC(12, 2) NOT NULL,
    usable_area_sqm NUMERIC(12, 2),
    bedrooms SMALLINT,
    bathrooms SMALLINT,
    floor_number SMALLINT,
    orientation VARCHAR(32),
    legal_status VARCHAR(150),
    list_price NUMERIC(18, 2),
    currency CHAR(3) NOT NULL DEFAULT 'VND',
    parcel_number VARCHAR(100),
    map_sheet_number VARCHAR(100),
    land_use_purpose VARCHAR(150),
    land_use_term VARCHAR(150),
    frontage_m NUMERIC(10, 2),
    road_width_m NUMERIC(10, 2),
    features JSONB NOT NULL DEFAULT '{}'::JSONB,
    published_at TIMESTAMPTZ,
    -- Last time the listing was confirmed still live, tracked apart from
    -- updated_at because any edit touches updated_at.
    last_verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT property_area_positive CHECK (area_sqm > 0),
    CONSTRAINT property_usable_area_positive CHECK (
        usable_area_sqm IS NULL OR usable_area_sqm > 0
    ),
    CONSTRAINT property_rooms_non_negative CHECK (
        (bedrooms IS NULL OR bedrooms >= 0)
        AND (bathrooms IS NULL OR bathrooms >= 0)
    ),
    CONSTRAINT property_price_non_negative CHECK (list_price IS NULL OR list_price >= 0),
    CONSTRAINT property_land_measurements_positive CHECK (
        (frontage_m IS NULL OR frontage_m > 0)
        AND (road_width_m IS NULL OR road_width_m > 0)
    ),
    CONSTRAINT property_geo_valid CHECK (
        (latitude IS NULL OR latitude BETWEEN -90 AND 90)
        AND (longitude IS NULL OR longitude BETWEEN -180 AND 180)
    )
);

CREATE TABLE external_sellers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(40) NOT NULL,
    source_seller_key VARCHAR(255) NOT NULL,
    source_account_id VARCHAR(100),
    display_name VARCHAR(200) NOT NULL,
    seller_type VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
    is_company BOOLEAN,
    source_verified BOOLEAN,
    is_professional BOOLEAN,
    profile_url TEXT,
    avatar_url TEXT,
    public_phone_masked VARCHAR(50),
    joined_text VARCHAR(100),
    active_listing_count INTEGER,
    rating NUMERIC(3, 2),
    has_zalo BOOLEAN,
    has_chat BOOLEAN,
    raw_data JSONB NOT NULL DEFAULT '{}'::JSONB,
    first_seen_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source, source_seller_key),
    CONSTRAINT external_seller_source_not_blank CHECK (length(trim(source)) > 0),
    CONSTRAINT external_seller_key_not_blank CHECK (length(trim(source_seller_key)) > 0),
    CONSTRAINT external_seller_name_not_blank CHECK (length(trim(display_name)) > 0),
    CONSTRAINT external_seller_type_valid CHECK (
        seller_type IN ('OWNER', 'BROKER', 'COMPANY', 'UNKNOWN')
    ),
    CONSTRAINT external_seller_rating_valid CHECK (rating IS NULL OR rating BETWEEN 0 AND 5),
    CONSTRAINT external_seller_listing_count_valid CHECK (
        active_listing_count IS NULL OR active_listing_count >= 0
    ),
    CONSTRAINT external_seller_seen_time_valid CHECK (last_seen_at >= first_seen_at)
);

CREATE UNIQUE INDEX uq_external_sellers_source_account
ON external_sellers(source, source_account_id)
WHERE source_account_id IS NOT NULL;

CREATE INDEX ix_external_sellers_source_name
ON external_sellers(source, display_name);

CREATE TABLE property_external_sellers (
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    external_seller_id UUID NOT NULL REFERENCES external_sellers(id) ON DELETE RESTRICT,
    relationship_type VARCHAR(30) NOT NULL DEFAULT 'LISTING_POSTER',
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    source_listing_id VARCHAR(150) NOT NULL,
    source_url TEXT NOT NULL,
    first_seen_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (property_id, external_seller_id),
    CONSTRAINT property_external_seller_relationship_valid CHECK (
        relationship_type IN ('LISTING_POSTER', 'OWNER', 'BROKER', 'COMPANY', 'UNKNOWN')
    ),
    CONSTRAINT property_external_seller_listing_id_not_blank CHECK (
        length(trim(source_listing_id)) > 0
    ),
    CONSTRAINT property_external_seller_url_not_blank CHECK (length(trim(source_url)) > 0),
    CONSTRAINT property_external_seller_seen_time_valid CHECK (last_seen_at >= first_seen_at)
);

CREATE UNIQUE INDEX uq_property_primary_external_seller
ON property_external_sellers(property_id)
WHERE is_primary;

CREATE INDEX ix_property_external_sellers_seller
ON property_external_sellers(external_seller_id, last_seen_at DESC);

CREATE TABLE property_media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    media_type VARCHAR(20) NOT NULL,
    url TEXT NOT NULL,
    source VARCHAR(40) NOT NULL DEFAULT 'INTERNAL',
    caption VARCHAR(255),
    sort_order SMALLINT NOT NULL DEFAULT 0,
    is_cover BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT property_media_type_valid CHECK (
        media_type IN ('IMAGE', 'VIDEO', 'FLOOR_PLAN', 'VIRTUAL_TOUR')
    ),
    CONSTRAINT property_media_source_not_blank CHECK (length(trim(source)) > 0),
    CONSTRAINT property_media_sort_valid CHECK (sort_order >= 0)
);

CREATE UNIQUE INDEX uq_property_cover_media
ON property_media(property_id) WHERE is_cover;

CREATE INDEX ix_property_media_source
ON property_media(property_id, source);

CREATE TABLE property_sale_assignments (
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    sale_user_id UUID NOT NULL REFERENCES sale_profiles(user_id) ON DELETE RESTRICT,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    unassigned_at TIMESTAMPTZ,
    PRIMARY KEY (property_id, sale_user_id),
    CONSTRAINT property_sale_assignment_time_valid CHECK (
        unassigned_at IS NULL OR unassigned_at > assigned_at
    )
);

CREATE UNIQUE INDEX uq_property_primary_sale
ON property_sale_assignments(property_id)
WHERE is_primary AND unassigned_at IS NULL;

CREATE TABLE sale_unavailability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sale_user_id UUID NOT NULL REFERENCES sale_profiles(user_id) ON DELETE CASCADE,
    unavailable_during TSTZRANGE NOT NULL,
    reason VARCHAR(255),
    source VARCHAR(30) NOT NULL DEFAULT 'INTERNAL',
    external_reference TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT sale_unavailability_nonempty CHECK (NOT isempty(unavailable_during)),
    CONSTRAINT sale_unavailability_source_valid CHECK (
        source IN ('INTERNAL', 'GOOGLE_CALENDAR', 'OUTLOOK_CALENDAR', 'SYSTEM')
    )
);

CREATE INDEX ix_sale_unavailability_range
ON sale_unavailability USING GIST (sale_user_id, unavailable_during);

-- ---------------------------------------------------------------------------
-- 11-15. AI conversation, tour request, proposed slot and HITL approval
-- ---------------------------------------------------------------------------

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_user_id UUID NOT NULL
        REFERENCES customer_profiles(user_id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    summary TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT conversation_status_valid CHECK (
        status IN ('OPEN', 'CLOSED', 'ARCHIVED')
    ),
    CONSTRAINT conversation_close_time_valid CHECK (
        closed_at IS NULL OR closed_at >= started_at
    )
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role message_role_t NOT NULL,
    content_redacted TEXT,
    structured_payload JSONB NOT NULL DEFAULT '{}'::JSONB,
    model_name VARCHAR(100),
    tool_call_id VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tour_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_code VARCHAR(32) NOT NULL UNIQUE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    customer_user_id UUID NOT NULL
        REFERENCES customer_profiles(user_id) ON DELETE RESTRICT,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    status request_status_t NOT NULL DEFAULT 'DRAFT',
    tour_mode tour_mode_t NOT NULL DEFAULT 'IN_PERSON',
    preferred_start TIMESTAMPTZ,
    preferred_end TIMESTAMPTZ,
    preferred_during TSTZRANGE GENERATED ALWAYS AS (
        CASE
            WHEN preferred_start IS NOT NULL AND preferred_end IS NOT NULL
            THEN tstzrange(preferred_start, preferred_end, '[)')
            ELSE NULL
        END
    ) STORED,
    party_size SMALLINT NOT NULL DEFAULT 1,
    customer_note TEXT,
    request_text_redacted TEXT,
    extracted_requirements JSONB NOT NULL DEFAULT '{}'::JSONB,
    submitted_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT tour_request_preference_pair CHECK (
        (preferred_start IS NULL AND preferred_end IS NULL)
        OR (
            preferred_start IS NOT NULL
            AND preferred_end IS NOT NULL
            AND preferred_end > preferred_start
        )
    ),
    CONSTRAINT tour_request_party_size_positive CHECK (party_size > 0),
    CONSTRAINT tour_request_expiry_valid CHECK (
        expires_at IS NULL OR expires_at > created_at
    ),
    UNIQUE (id, customer_user_id, property_id)
);

CREATE TABLE tour_slot_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tour_request_id UUID NOT NULL REFERENCES tour_requests(id) ON DELETE CASCADE,
    sale_user_id UUID NOT NULL REFERENCES sale_profiles(user_id) ON DELETE RESTRICT,
    status slot_status_t NOT NULL DEFAULT 'PROPOSED',
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    slot_during TSTZRANGE GENERATED ALWAYS AS (
        tstzrange(starts_at, ends_at, '[)')
    ) STORED,
    meeting_address TEXT,
    waiting_room_name VARCHAR(100),
    score NUMERIC(7, 4),
    score_explanation JSONB NOT NULL DEFAULT '{}'::JSONB,
    valid_until TIMESTAMPTZ NOT NULL,
    selected_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT tour_slot_time_valid CHECK (ends_at > starts_at),
    CONSTRAINT tour_slot_validity_time CHECK (valid_until > created_at),
    CONSTRAINT tour_slot_score_valid CHECK (score IS NULL OR score BETWEEN 0 AND 100),
    CONSTRAINT tour_slot_selected_at_valid CHECK (
        status <> 'SELECTED' OR selected_at IS NOT NULL
    ),
    UNIQUE (id, tour_request_id)
);

CREATE UNIQUE INDEX uq_one_selected_slot_per_request
ON tour_slot_options(tour_request_id) WHERE status = 'SELECTED';

CREATE TABLE approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tour_request_id UUID NOT NULL REFERENCES tour_requests(id) ON DELETE CASCADE,
    slot_option_id UUID NOT NULL,
    requested_reviewer_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status approval_status_t NOT NULL DEFAULT 'PENDING',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    decided_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    decided_at TIMESTAMPTZ,
    decision_note TEXT,
    approved_sale_user_id UUID REFERENCES sale_profiles(user_id) ON DELETE RESTRICT,
    approved_starts_at TIMESTAMPTZ,
    approved_ends_at TIMESTAMPTZ,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT approval_expiry_valid CHECK (expires_at > requested_at),
    CONSTRAINT approval_version_positive CHECK (version > 0),
    CONSTRAINT approval_decision_valid CHECK (
        (status = 'PENDING' AND decided_at IS NULL)
        OR (status <> 'PENDING' AND decided_at IS NOT NULL)
    ),
    CONSTRAINT approval_booking_fields_valid CHECK (
        status <> 'APPROVED'
        OR (
            approved_sale_user_id IS NOT NULL
            AND approved_starts_at IS NOT NULL
            AND approved_ends_at IS NOT NULL
            AND approved_ends_at > approved_starts_at
        )
    ),
    CONSTRAINT approval_slot_matches_request
        FOREIGN KEY (slot_option_id, tour_request_id)
        REFERENCES tour_slot_options(id, tour_request_id) ON DELETE RESTRICT,
    UNIQUE (id, tour_request_id)
);

CREATE UNIQUE INDEX uq_one_pending_approval_per_request
ON approval_requests(tour_request_id) WHERE status = 'PENDING';

-- ---------------------------------------------------------------------------
-- 16-18. Confirmed appointment, temporary property hold and notifications
-- ---------------------------------------------------------------------------

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_code VARCHAR(32) NOT NULL UNIQUE,
    tour_request_id UUID NOT NULL UNIQUE,
    approval_request_id UUID NOT NULL UNIQUE,
    customer_user_id UUID NOT NULL
        REFERENCES customer_profiles(user_id) ON DELETE RESTRICT,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    sale_user_id UUID NOT NULL REFERENCES sale_profiles(user_id) ON DELETE RESTRICT,
    status appointment_status_t NOT NULL DEFAULT 'CONFIRMED',
    tour_mode tour_mode_t NOT NULL DEFAULT 'IN_PERSON',
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    appointment_during TSTZRANGE GENERATED ALWAYS AS (
        tstzrange(starts_at, ends_at, '[)')
    ) STORED,
    party_size SMALLINT NOT NULL DEFAULT 1,
    meeting_address TEXT,
    waiting_room_name VARCHAR(100),
    customer_note TEXT,
    internal_note TEXT,
    external_calendar_event_id TEXT,
    calendar_sync_status sync_status_t NOT NULL DEFAULT 'NOT_REQUESTED',
    calendar_sync_error TEXT,
    confirmation_sent_at TIMESTAMPTZ,
    checked_in_at TIMESTAMPTZ,
    checked_out_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    cancellation_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT appointment_time_valid CHECK (ends_at > starts_at),
    CONSTRAINT appointment_party_size_positive CHECK (party_size > 0),
    CONSTRAINT appointment_checkout_valid CHECK (
        checked_out_at IS NULL
        OR (checked_in_at IS NOT NULL AND checked_out_at >= checked_in_at)
    ),
    CONSTRAINT appointment_cancel_valid CHECK (
        status <> 'CANCELLED' OR cancelled_at IS NOT NULL
    ),
    CONSTRAINT appointment_matches_request
        FOREIGN KEY (tour_request_id, customer_user_id, property_id)
        REFERENCES tour_requests(id, customer_user_id, property_id) ON DELETE RESTRICT,
    CONSTRAINT appointment_matches_approval
        FOREIGN KEY (approval_request_id, tour_request_id)
        REFERENCES approval_requests(id, tour_request_id) ON DELETE RESTRICT,
    EXCLUDE USING GIST (
        sale_user_id WITH =,
        appointment_during WITH &&
    ) WHERE (status IN ('CONFIRMED', 'IN_PROGRESS')),
    EXCLUDE USING GIST (
        property_id WITH =,
        appointment_during WITH &&
    ) WHERE (status IN ('CONFIRMED', 'IN_PROGRESS')),
    UNIQUE (id, property_id, customer_user_id)
);

CREATE OR REPLACE FUNCTION validate_approved_appointment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    approval_row approval_requests%ROWTYPE;
    current_property_status property_status_t;
BEGIN
    SELECT * INTO approval_row
    FROM approval_requests
    WHERE id = NEW.approval_request_id
      AND tour_request_id = NEW.tour_request_id;

    IF approval_row.status IS DISTINCT FROM 'APPROVED'::approval_status_t THEN
        RAISE EXCEPTION 'Appointment requires an approved HITL request';
    END IF;

    IF NEW.sale_user_id IS DISTINCT FROM approval_row.approved_sale_user_id
       OR NEW.starts_at IS DISTINCT FROM approval_row.approved_starts_at
       OR NEW.ends_at IS DISTINCT FROM approval_row.approved_ends_at THEN
        RAISE EXCEPTION 'Appointment details must match the sale-approved details';
    END IF;

    SELECT status INTO current_property_status
    FROM properties
    WHERE id = NEW.property_id;

    IF current_property_status NOT IN ('AVAILABLE', 'UNDER_OFFER') THEN
        RAISE EXCEPTION 'Property % is not available for a viewing', NEW.property_id;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM sale_unavailability su
        WHERE su.sale_user_id = NEW.sale_user_id
          AND su.unavailable_during && tstzrange(NEW.starts_at, NEW.ends_at, '[)')
    ) THEN
        RAISE EXCEPTION 'Sale % is unavailable during the requested time', NEW.sale_user_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validate_approved_appointment
BEFORE INSERT OR UPDATE OF
    approval_request_id, sale_user_id, property_id, starts_at, ends_at
ON appointments
FOR EACH ROW EXECUTE FUNCTION validate_approved_appointment();

CREATE TABLE property_holds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hold_code VARCHAR(32) NOT NULL UNIQUE,
    appointment_id UUID NOT NULL UNIQUE
        REFERENCES appointments(id) ON DELETE RESTRICT,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE RESTRICT,
    customer_user_id UUID NOT NULL
        REFERENCES customer_profiles(user_id) ON DELETE RESTRICT,
    approved_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status hold_status_t NOT NULL DEFAULT 'ACTIVE',
    starts_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    max_expires_at TIMESTAMPTZ NOT NULL,
    extension_count SMALLINT NOT NULL DEFAULT 0,
    released_at TIMESTAMPTZ,
    release_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT property_hold_time_valid CHECK (
        expires_at > starts_at AND max_expires_at >= expires_at
    ),
    CONSTRAINT property_hold_extension_valid CHECK (extension_count >= 0),
    CONSTRAINT property_hold_release_valid CHECK (
        status = 'ACTIVE' OR released_at IS NOT NULL
    ),
    CONSTRAINT property_hold_matches_appointment
        FOREIGN KEY (appointment_id, property_id, customer_user_id)
        REFERENCES appointments(id, property_id, customer_user_id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_one_active_hold_per_property
ON property_holds(property_id) WHERE status = 'ACTIVE';

CREATE INDEX ix_property_holds_expiry
ON property_holds(expires_at) WHERE status = 'ACTIVE';

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    appointment_id UUID REFERENCES appointments(id) ON DELETE CASCADE,
    channel notification_channel_t NOT NULL,
    template_key VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::JSONB,
    scheduled_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    status delivery_status_t NOT NULL DEFAULT 'PENDING',
    retry_count SMALLINT NOT NULL DEFAULT 0,
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT notification_retry_valid CHECK (retry_count >= 0)
);

-- ---------------------------------------------------------------------------
-- Transactional soft-hold and lifecycle helpers
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION create_property_hold(
    p_appointment_id UUID,
    p_approved_by_user_id UUID,
    p_hold_minutes SMALLINT DEFAULT NULL
)
RETURNS property_holds
LANGUAGE plpgsql
AS $$
DECLARE
    appointment_row appointments%ROWTYPE;
    project_row projects%ROWTYPE;
    hold_row property_holds%ROWTYPE;
    effective_minutes SMALLINT;
BEGIN
    SELECT * INTO appointment_row
    FROM appointments
    WHERE id = p_appointment_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Appointment % does not exist', p_appointment_id;
    END IF;

    -- Row lock serializes concurrent hold attempts for the same property.
    PERFORM 1 FROM properties
    WHERE id = appointment_row.property_id
    FOR UPDATE;

    UPDATE property_holds
    SET status = 'EXPIRED',
        released_at = now(),
        release_reason = COALESCE(release_reason, 'AUTO_EXPIRED'),
        updated_at = now()
    WHERE property_id = appointment_row.property_id
      AND status = 'ACTIVE'
      AND expires_at <= now();

    IF EXISTS (
        SELECT 1 FROM property_holds
        WHERE property_id = appointment_row.property_id
          AND status = 'ACTIVE'
    ) THEN
        RAISE EXCEPTION 'Property % already has an active hold', appointment_row.property_id;
    END IF;

    SELECT pr.* INTO project_row
    FROM properties p
    LEFT JOIN projects pr ON pr.id = p.project_id
    WHERE p.id = appointment_row.property_id;

    effective_minutes := COALESCE(
        p_hold_minutes,
        project_row.default_hold_minutes,
        30
    );

    IF effective_minutes <= 0 THEN
        RAISE EXCEPTION 'Hold duration must be positive';
    END IF;

    INSERT INTO property_holds (
        hold_code,
        appointment_id,
        property_id,
        customer_user_id,
        approved_by_user_id,
        expires_at,
        max_expires_at
    ) VALUES (
        'HOLD-' || upper(substr(replace(gen_random_uuid()::TEXT, '-', ''), 1, 12)),
        appointment_row.id,
        appointment_row.property_id,
        appointment_row.customer_user_id,
        p_approved_by_user_id,
        now() + make_interval(mins => effective_minutes),
        now() + make_interval(
            mins => effective_minutes * (1 + COALESCE(project_row.max_hold_extensions, 1))
        )
    )
    RETURNING * INTO hold_row;

    RETURN hold_row;
END;
$$;

CREATE OR REPLACE FUNCTION expire_stale_booking_records(
    cutoff TIMESTAMPTZ DEFAULT now()
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    expired_slots INTEGER;
    expired_approvals INTEGER;
    expired_holds INTEGER;
BEGIN
    UPDATE tour_slot_options
    SET status = 'EXPIRED', updated_at = cutoff
    WHERE status = 'PROPOSED' AND valid_until <= cutoff;
    GET DIAGNOSTICS expired_slots = ROW_COUNT;

    UPDATE approval_requests
    SET status = 'EXPIRED',
        decided_at = cutoff,
        version = version + 1,
        updated_at = cutoff
    WHERE status = 'PENDING' AND expires_at <= cutoff;
    GET DIAGNOSTICS expired_approvals = ROW_COUNT;

    UPDATE property_holds
    SET status = 'EXPIRED',
        released_at = cutoff,
        release_reason = COALESCE(release_reason, 'AUTO_EXPIRED'),
        updated_at = cutoff
    WHERE status = 'ACTIVE' AND expires_at <= cutoff;
    GET DIAGNOSTICS expired_holds = ROW_COUNT;

    RETURN jsonb_build_object(
        'slots', expired_slots,
        'approvals', expired_approvals,
        'holds', expired_holds
    );
END;
$$;

CREATE OR REPLACE FUNCTION release_hold_after_appointment_close()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.status IN ('CANCELLED', 'RESCHEDULED')
       AND OLD.status IS DISTINCT FROM NEW.status THEN
        UPDATE property_holds
        SET status = 'RELEASED',
            released_at = now(),
            release_reason = 'APPOINTMENT_' || NEW.status::TEXT,
            updated_at = now()
        WHERE appointment_id = NEW.id AND status = 'ACTIVE';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_release_hold_after_appointment_close
AFTER UPDATE OF status ON appointments
FOR EACH ROW EXECUTE FUNCTION release_hold_after_appointment_close();

-- ---------------------------------------------------------------------------
-- Indexes and API views
-- ---------------------------------------------------------------------------

CREATE INDEX ix_properties_search
ON properties(project_id, status, property_kind, list_price);

CREATE INDEX ix_property_assignments_sale
ON property_sale_assignments(sale_user_id)
WHERE unassigned_at IS NULL;

CREATE INDEX ix_messages_conversation_timeline
ON messages(conversation_id, created_at);

CREATE INDEX ix_tour_requests_customer_status
ON tour_requests(customer_user_id, status, created_at DESC);

CREATE INDEX ix_tour_requests_property_status
ON tour_requests(property_id, status);

CREATE INDEX ix_tour_requests_preferred_range
ON tour_requests USING GIST (preferred_during);

CREATE INDEX ix_tour_slot_options_request
ON tour_slot_options(tour_request_id, status, starts_at);

CREATE INDEX ix_approval_queue
ON approval_requests(requested_reviewer_user_id, expires_at)
WHERE status = 'PENDING';

CREATE INDEX ix_appointments_customer
ON appointments(customer_user_id, starts_at DESC);

CREATE INDEX ix_appointments_sale
ON appointments(sale_user_id, starts_at);

CREATE INDEX ix_appointments_property
ON appointments(property_id, starts_at);

CREATE INDEX ix_notifications_due
ON notifications(scheduled_at) WHERE status = 'PENDING';

CREATE VIEW v_property_live_status AS
SELECT
    p.id,
    p.code,
    p.title,
    p.project_id,
    p.property_kind,
    p.status AS inventory_status,
    CASE
        WHEN p.status = 'AVAILABLE' AND h.expires_at IS NOT NULL THEN 'SOFT_HELD'
        ELSE p.status::TEXT
    END AS live_status,
    h.hold_code,
    h.expires_at AS hold_expires_at
FROM properties p
LEFT JOIN LATERAL (
    SELECT hold_code, expires_at
    FROM property_holds
    WHERE property_id = p.id
      AND status = 'ACTIVE'
      AND expires_at > now()
    LIMIT 1
) h ON TRUE;

CREATE VIEW v_sale_daily_schedule AS
SELECT
    a.sale_user_id,
    u.full_name AS sale_name,
    (a.starts_at AT TIME ZONE u.timezone)::DATE AS local_date,
    a.id AS appointment_id,
    a.booking_code,
    a.starts_at,
    a.ends_at,
    a.status,
    p.code AS property_code,
    p.title AS property_title,
    a.meeting_address
FROM appointments a
JOIN users u ON u.id = a.sale_user_id
JOIN properties p ON p.id = a.property_id
WHERE a.status IN ('CONFIRMED', 'IN_PROGRESS');

-- updated_at triggers
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_customer_profiles_updated_at
BEFORE UPDATE ON customer_profiles
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_sale_profiles_updated_at
BEFORE UPDATE ON sale_profiles
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_projects_updated_at
BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_properties_updated_at
BEFORE UPDATE ON properties
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_external_sellers_updated_at
BEFORE UPDATE ON external_sellers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_property_external_sellers_updated_at
BEFORE UPDATE ON property_external_sellers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_conversations_updated_at
BEFORE UPDATE ON conversations
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_tour_requests_updated_at
BEFORE UPDATE ON tour_requests
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_tour_slot_options_updated_at
BEFORE UPDATE ON tour_slot_options
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_approval_requests_updated_at
BEFORE UPDATE ON approval_requests
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_appointments_updated_at
BEFORE UPDATE ON appointments
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_property_holds_updated_at
BEFORE UPDATE ON property_holds
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMIT;
