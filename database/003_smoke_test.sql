-- Constraint smoke test for the canonical 18-table MVP database.
-- Requires 001, 002, 004 and 005 in that order.
-- The transaction is rolled back, so no test data remains.

BEGIN;

DO $$
DECLARE
    missing_tables TEXT;
    user_count INTEGER;
    customer_count INTEGER;
    sale_count INTEGER;
    seller_count INTEGER;
    seller_link_count INTEGER;
    property_count INTEGER;
    media_count INTEGER;
    nhatot_property_count INTEGER;
    batdongsan_property_count INTEGER;
    nhatot_seller_count INTEGER;
    batdongsan_seller_count INTEGER;
    nhatot_media_count INTEGER;
    batdongsan_media_count INTEGER;
    unknown_source_count INTEGER;
    invalid_batdongsan_media_count INTEGER;
    missing_batdongsan_phone_count INTEGER;
    missing_external_seller_count INTEGER;
    missing_primary_sale_count INTEGER;
BEGIN
    -- The canonical 18 must all exist. Counting them instead would fail every
    -- time a feature adds a table, which says nothing about the MVP schema.
    SELECT string_agg(expected.name, ', ' ORDER BY expected.name) INTO missing_tables
    FROM unnest(ARRAY[
        'users', 'customer_profiles', 'sale_profiles', 'projects', 'properties',
        'external_sellers', 'property_external_sellers', 'property_media',
        'property_sale_assignments', 'sale_unavailability', 'conversations',
        'messages', 'tour_requests', 'tour_slot_options', 'approval_requests',
        'appointments', 'property_holds', 'notifications'
    ]) AS expected(name)
    WHERE NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
          AND table_name = expected.name
    );

    -- Only the seeded demo accounts, identified by their fixed UUID block. A
    -- long-lived dev database also holds accounts created by hand, and counting
    -- those would make the assertion drift instead of catching a broken seed.
    SELECT count(*) INTO user_count FROM users
    WHERE id BETWEEN '10000000-0000-0000-0000-000000000001'
                 AND '10000000-0000-0000-0000-0000000000ff';
    SELECT count(*) INTO customer_count FROM customer_profiles
    WHERE user_id BETWEEN '10000000-0000-0000-0000-000000000001'
                      AND '10000000-0000-0000-0000-0000000000ff';
    SELECT count(*) INTO sale_count FROM sale_profiles
    WHERE user_id BETWEEN '10000000-0000-0000-0000-000000000001'
                      AND '10000000-0000-0000-0000-0000000000ff';
    SELECT count(*) INTO seller_count FROM external_sellers;
    SELECT count(*) INTO seller_link_count FROM property_external_sellers;
    SELECT count(*) INTO property_count FROM properties;
    SELECT count(*) INTO media_count FROM property_media;
    SELECT count(*) INTO nhatot_property_count
    FROM properties WHERE features->>'source' = 'NHATOT';
    SELECT count(*) INTO batdongsan_property_count
    FROM properties WHERE features->>'source' = 'BATDONGSAN_COM_VN';
    SELECT count(*) INTO nhatot_seller_count
    FROM external_sellers WHERE source = 'NHATOT';
    SELECT count(*) INTO batdongsan_seller_count
    FROM external_sellers WHERE source = 'BATDONGSAN_COM_VN';
    SELECT count(*) INTO nhatot_media_count
    FROM property_media WHERE source = 'NHATOT';
    SELECT count(*) INTO batdongsan_media_count
    FROM property_media WHERE source = 'BATDONGSAN_COM_VN';

    IF missing_tables IS NOT NULL THEN
        RAISE EXCEPTION 'Missing canonical MVP tables: %', missing_tables;
    END IF;
    IF user_count <> 10 OR customer_count <> 5 OR sale_count <> 3 THEN
        RAISE EXCEPTION 'Unexpected demo account seed counts: users=%, customers=%, sales=%',
            user_count, customer_count, sale_count;
    END IF;
    -- Batch size changes on every re-crawl, so assert the shape of the batch
    -- rather than its size: every listing keeps at least three photos, and no
    -- batch can carry more distinct posters than listings.
    IF nhatot_property_count < 1 OR nhatot_seller_count < 1
       OR nhatot_media_count < nhatot_property_count * 3
       OR nhatot_seller_count > nhatot_property_count THEN
        RAISE EXCEPTION 'Incomplete Nha Tot batch: properties=%, sellers=%, media=%',
            nhatot_property_count, nhatot_seller_count, nhatot_media_count;
    END IF;
    IF batdongsan_property_count < 1 OR batdongsan_seller_count < 1
       OR batdongsan_media_count < batdongsan_property_count * 3 THEN
        RAISE EXCEPTION 'Incomplete Batdongsan batch: properties=%, sellers=%, media=%',
            batdongsan_property_count, batdongsan_seller_count, batdongsan_media_count;
    END IF;
    IF seller_count <> nhatot_seller_count + batdongsan_seller_count
       OR seller_link_count <> nhatot_property_count + batdongsan_property_count THEN
        RAISE EXCEPTION 'Unexpected external seller totals: sellers=%, links=%',
            seller_count, seller_link_count;
    END IF;
    -- Totals move with every crawl, so the useful assertion is that nothing
    -- carries a source outside the two known crawlers. A typo in a crawler's
    -- source tag would otherwise slip in unnoticed.
    SELECT count(*) INTO unknown_source_count
    FROM properties
    WHERE features ? 'source'
      AND features->>'source' NOT IN ('NHATOT', 'BATDONGSAN_COM_VN');
    IF unknown_source_count <> 0 THEN
        RAISE EXCEPTION '% properties carry an unknown crawl source',
            unknown_source_count;
    END IF;
    IF property_count < nhatot_property_count + batdongsan_property_count
       OR media_count < nhatot_media_count + batdongsan_media_count THEN
        RAISE EXCEPTION 'Inventory totals below their crawled parts: properties=%, media=%',
            property_count, media_count;
    END IF;

    SELECT count(*) INTO invalid_batdongsan_media_count
    FROM (
        SELECT property.id
        FROM properties property
        LEFT JOIN property_media media
          ON media.property_id = property.id
         AND media.source = 'BATDONGSAN_COM_VN'
         AND media.media_type = 'IMAGE'
        WHERE property.features->>'source' = 'BATDONGSAN_COM_VN'
        GROUP BY property.id
        HAVING count(media.id) < 3
            OR count(media.id) <> count(DISTINCT media.url)
            OR count(media.id) FILTER (WHERE media.is_cover) <> 1
    ) invalid_media;
    IF invalid_batdongsan_media_count <> 0 THEN
        RAISE EXCEPTION '% Batdongsan properties have invalid media',
            invalid_batdongsan_media_count;
    END IF;

    SELECT count(*) INTO missing_batdongsan_phone_count
    FROM property_external_sellers relation
    JOIN external_sellers seller ON seller.id = relation.external_seller_id
    WHERE relation.is_primary
      AND seller.source = 'BATDONGSAN_COM_VN'
      AND (
          nullif(trim(seller.public_phone_masked), '') IS NULL
          OR position('*' IN seller.public_phone_masked) = 0
      );
    IF missing_batdongsan_phone_count <> 0 THEN
        RAISE EXCEPTION '% Batdongsan properties have no masked seller phone',
            missing_batdongsan_phone_count;
    END IF;

    SELECT count(*) INTO missing_external_seller_count
    FROM properties property
    WHERE property.features ? 'source'
      AND NOT EXISTS (
          SELECT 1
          FROM property_external_sellers relation
          WHERE relation.property_id = property.id
            AND relation.is_primary
      );
    IF missing_external_seller_count <> 0 THEN
        RAISE EXCEPTION '% crawled properties have no primary external seller',
            missing_external_seller_count;
    END IF;

    SELECT count(*) INTO missing_primary_sale_count
    FROM properties property
    WHERE NOT EXISTS (
        SELECT 1
        FROM property_sale_assignments assignment
        WHERE assignment.property_id = property.id
          AND assignment.is_primary
          AND assignment.unassigned_at IS NULL
    );
    IF missing_primary_sale_count <> 0 THEN
        RAISE EXCEPTION '% properties have no active primary internal sale',
            missing_primary_sale_count;
    END IF;

    RAISE NOTICE 'PASS: canonical 18 tables present, demo seed intact, seller/sale links complete';
END;
$$;

-- The constraint tests below need one known property. Nothing in 001, 002, 004
-- or 005 creates it, so the test owns its own fixture; the whole file is rolled
-- back, and the deterministic UUID keeps it out of the crawled ranges.
INSERT INTO properties (
    id, code, property_kind, title, status, area_sqm, list_price, currency
) VALUES (
    '40000000-0000-0000-0000-000000000001',
    'SMOKE-FIXTURE-001',
    'APARTMENT',
    'Căn mẫu dùng cho smoke test',
    'AVAILABLE',
    70.00,
    3500000000.00,
    'VND'
);

INSERT INTO property_sale_assignments (property_id, sale_user_id, is_primary, assigned_at)
VALUES (
    '40000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000002',
    TRUE,
    now()
);

INSERT INTO conversations (id, customer_user_id)
VALUES (
    '80000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001'
);

INSERT INTO tour_requests (
    id, request_code, conversation_id, customer_user_id, property_id,
    status, preferred_start, preferred_end, party_size, submitted_at
) VALUES (
    '80000000-0000-0000-0000-000000000002',
    'REQ-SMOKE-001',
    '80000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    'APPROVED',
    now() + INTERVAL '7 days 2 hours',
    now() + INTERVAL '7 days 4 hours',
    2,
    now()
);

INSERT INTO tour_slot_options (
    id, tour_request_id, sale_user_id, status,
    starts_at, ends_at, score, valid_until, selected_at
) VALUES (
    '80000000-0000-0000-0000-000000000003',
    '80000000-0000-0000-0000-000000000002',
    '10000000-0000-0000-0000-000000000002',
    'SELECTED',
    now() + INTERVAL '7 days 2 hours 30 minutes',
    now() + INTERVAL '7 days 3 hours 30 minutes',
    92.5,
    now() + INTERVAL '1 day',
    now()
);

INSERT INTO approval_requests (
    id, tour_request_id, slot_option_id, requested_reviewer_user_id,
    status, requested_at, expires_at, decided_by_user_id, decided_at,
    approved_sale_user_id, approved_starts_at, approved_ends_at
) VALUES (
    '80000000-0000-0000-0000-000000000004',
    '80000000-0000-0000-0000-000000000002',
    '80000000-0000-0000-0000-000000000003',
    '10000000-0000-0000-0000-000000000002',
    'APPROVED',
    now(), now() + INTERVAL '15 minutes',
    '10000000-0000-0000-0000-000000000002', now(),
    '10000000-0000-0000-0000-000000000002',
    now() + INTERVAL '7 days 2 hours 30 minutes',
    now() + INTERVAL '7 days 3 hours 30 minutes'
);

INSERT INTO appointments (
    id, booking_code, tour_request_id, approval_request_id,
    customer_user_id, property_id, sale_user_id,
    starts_at, ends_at, party_size, meeting_address
) VALUES (
    '80000000-0000-0000-0000-000000000005',
    'BOOK-SMOKE-001',
    '80000000-0000-0000-0000-000000000002',
    '80000000-0000-0000-0000-000000000004',
    '10000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000002',
    now() + INTERVAL '7 days 2 hours 30 minutes',
    now() + INTERVAL '7 days 3 hours 30 minutes',
    2,
    'Sunrise Riverside'
);

INSERT INTO property_holds (
    id, hold_code, appointment_id, property_id, customer_user_id,
    approved_by_user_id, starts_at, expires_at, max_expires_at
) VALUES (
    '80000000-0000-0000-0000-000000000006',
    'HOLD-SMOKE-001',
    '80000000-0000-0000-0000-000000000005',
    '40000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000002',
    now(), now() + INTERVAL '30 minutes', now() + INTERVAL '45 minutes'
);

-- Prepare a second request whose time overlaps the first appointment.
INSERT INTO tour_requests (
    id, request_code, conversation_id, customer_user_id, property_id,
    status, preferred_start, preferred_end, party_size, submitted_at
) VALUES (
    '80000000-0000-0000-0000-000000000012',
    'REQ-SMOKE-002',
    '80000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    'WAITING_APPROVAL',
    now() + INTERVAL '7 days 3 hours',
    now() + INTERVAL '7 days 4 hours',
    2,
    now()
);

INSERT INTO tour_slot_options (
    id, tour_request_id, sale_user_id, status,
    starts_at, ends_at, score, valid_until, selected_at
) VALUES (
    '80000000-0000-0000-0000-000000000013',
    '80000000-0000-0000-0000-000000000012',
    '10000000-0000-0000-0000-000000000002',
    'SELECTED',
    now() + INTERVAL '7 days 3 hours',
    now() + INTERVAL '7 days 4 hours',
    80,
    now() + INTERVAL '1 day',
    now()
);

INSERT INTO approval_requests (
    id, tour_request_id, slot_option_id, requested_reviewer_user_id,
    status, requested_at, expires_at
) VALUES (
    '80000000-0000-0000-0000-000000000014',
    '80000000-0000-0000-0000-000000000012',
    '80000000-0000-0000-0000-000000000013',
    '10000000-0000-0000-0000-000000000002',
    'PENDING',
    now(), now() + INTERVAL '15 minutes'
);

DO $$
BEGIN
    BEGIN
        INSERT INTO appointments (
            id, booking_code, tour_request_id, approval_request_id,
            customer_user_id, property_id, sale_user_id,
            starts_at, ends_at, party_size
        ) VALUES (
            '80000000-0000-0000-0000-000000000015',
            'BOOK-SMOKE-002',
            '80000000-0000-0000-0000-000000000012',
            '80000000-0000-0000-0000-000000000014',
            '10000000-0000-0000-0000-000000000001',
            '40000000-0000-0000-0000-000000000001',
            '10000000-0000-0000-0000-000000000002',
            now() + INTERVAL '7 days 3 hours',
            now() + INTERVAL '7 days 4 hours',
            2
        );
        RAISE EXCEPTION USING
            ERRCODE = 'check_violation',
            MESSAGE = 'Expected pending HITL approval rejection was not raised';
    EXCEPTION
        WHEN raise_exception THEN
            RAISE NOTICE 'PASS: appointment cannot be created before HITL approval';
    END;

    UPDATE approval_requests
    SET status = 'APPROVED',
        decided_by_user_id = '10000000-0000-0000-0000-000000000002',
        decided_at = now(),
        approved_sale_user_id = '10000000-0000-0000-0000-000000000002',
        approved_starts_at = now() + INTERVAL '7 days 3 hours',
        approved_ends_at = now() + INTERVAL '7 days 4 hours'
    WHERE id = '80000000-0000-0000-0000-000000000014';

    BEGIN
        INSERT INTO appointments (
            id, booking_code, tour_request_id, approval_request_id,
            customer_user_id, property_id, sale_user_id,
            starts_at, ends_at, party_size
        ) VALUES (
            '80000000-0000-0000-0000-000000000015',
            'BOOK-SMOKE-002',
            '80000000-0000-0000-0000-000000000012',
            '80000000-0000-0000-0000-000000000014',
            '10000000-0000-0000-0000-000000000001',
            '40000000-0000-0000-0000-000000000001',
            '10000000-0000-0000-0000-000000000002',
            now() + INTERVAL '7 days 3 hours',
            now() + INTERVAL '7 days 4 hours',
            2
        );
        RAISE EXCEPTION 'Expected exclusion_violation was not raised';
    EXCEPTION
        WHEN exclusion_violation THEN
            RAISE NOTICE 'PASS: overlapping sale/property booking was rejected';
    END;

    BEGIN
        UPDATE appointments
        SET starts_at = now() + INTERVAL '7 days 2 hours 45 minutes'
        WHERE id = '80000000-0000-0000-0000-000000000005';
        RAISE EXCEPTION USING
            ERRCODE = 'check_violation',
            MESSAGE = 'Expected HITL validation error was not raised';
    EXCEPTION
        WHEN raise_exception THEN
            RAISE NOTICE 'PASS: appointment details cannot differ from sale approval';
    END;
END;
$$;

ROLLBACK;
