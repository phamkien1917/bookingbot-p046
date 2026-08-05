-- Constraint smoke test. Requires 001_schema.sql and 002_seed.sql.
-- The transaction is rolled back, so no test data remains.

BEGIN;

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
    '2030-01-05T02:00:00Z',
    '2030-01-05T04:00:00Z',
    2,
    now()
);

INSERT INTO tour_slot_options (
    id, tour_request_id, sale_user_id, vehicle_id, status,
    starts_at, ends_at, score, valid_until, selected_at
) VALUES (
    '80000000-0000-0000-0000-000000000003',
    '80000000-0000-0000-0000-000000000002',
    '10000000-0000-0000-0000-000000000002',
    '20000000-0000-0000-0000-000000000001',
    'SELECTED',
    '2030-01-05T02:30:00Z',
    '2030-01-05T03:30:00Z',
    92.5,
    '2030-01-05T02:00:00Z',
    now()
);

INSERT INTO approval_requests (
    id, tour_request_id, slot_option_id, requested_reviewer_user_id,
    status, requested_at, expires_at, decided_by_user_id, decided_at,
    approved_sale_user_id, approved_vehicle_id,
    approved_starts_at, approved_ends_at
) VALUES (
    '80000000-0000-0000-0000-000000000004',
    '80000000-0000-0000-0000-000000000002',
    '80000000-0000-0000-0000-000000000003',
    '10000000-0000-0000-0000-000000000002',
    'APPROVED',
    now(), now() + INTERVAL '15 minutes',
    '10000000-0000-0000-0000-000000000002', now(),
    '10000000-0000-0000-0000-000000000002',
    '20000000-0000-0000-0000-000000000001',
    '2030-01-05T02:30:00Z',
    '2030-01-05T03:30:00Z'
);

INSERT INTO appointments (
    id, booking_code, tour_request_id, approval_request_id,
    customer_user_id, property_id, sale_user_id, vehicle_id,
    starts_at, ends_at, party_size, meeting_address
) VALUES (
    '80000000-0000-0000-0000-000000000005',
    'BOOK-SMOKE-001',
    '80000000-0000-0000-0000-000000000002',
    '80000000-0000-0000-0000-000000000004',
    '10000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000002',
    '20000000-0000-0000-0000-000000000001',
    '2030-01-05T02:30:00Z',
    '2030-01-05T03:30:00Z',
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

-- Prepare a second, fully approved request whose time overlaps the first one.
INSERT INTO tour_requests (
    id, request_code, conversation_id, customer_user_id, property_id,
    status, preferred_start, preferred_end, party_size, submitted_at
) VALUES (
    '80000000-0000-0000-0000-000000000012',
    'REQ-SMOKE-002',
    '80000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    'APPROVED',
    '2030-01-05T03:00:00Z',
    '2030-01-05T04:00:00Z',
    2,
    now()
);

INSERT INTO tour_slot_options (
    id, tour_request_id, sale_user_id, vehicle_id, status,
    starts_at, ends_at, score, valid_until, selected_at
) VALUES (
    '80000000-0000-0000-0000-000000000013',
    '80000000-0000-0000-0000-000000000012',
    '10000000-0000-0000-0000-000000000002',
    '20000000-0000-0000-0000-000000000001',
    'SELECTED',
    '2030-01-05T03:00:00Z',
    '2030-01-05T04:00:00Z',
    80,
    '2030-01-05T02:30:00Z',
    now()
);

INSERT INTO approval_requests (
    id, tour_request_id, slot_option_id, requested_reviewer_user_id,
    status, requested_at, expires_at, decided_by_user_id, decided_at,
    approved_sale_user_id, approved_vehicle_id,
    approved_starts_at, approved_ends_at
) VALUES (
    '80000000-0000-0000-0000-000000000014',
    '80000000-0000-0000-0000-000000000012',
    '80000000-0000-0000-0000-000000000013',
    '10000000-0000-0000-0000-000000000002',
    'APPROVED',
    now(), now() + INTERVAL '15 minutes',
    '10000000-0000-0000-0000-000000000002', now(),
    '10000000-0000-0000-0000-000000000002',
    '20000000-0000-0000-0000-000000000001',
    '2030-01-05T03:00:00Z',
    '2030-01-05T04:00:00Z'
);

DO $$
BEGIN
    BEGIN
        INSERT INTO appointments (
            id, booking_code, tour_request_id, approval_request_id,
            customer_user_id, property_id, sale_user_id, vehicle_id,
            starts_at, ends_at, party_size
        ) VALUES (
            '80000000-0000-0000-0000-000000000015',
            'BOOK-SMOKE-002',
            '80000000-0000-0000-0000-000000000012',
            '80000000-0000-0000-0000-000000000014',
            '10000000-0000-0000-0000-000000000001',
            '40000000-0000-0000-0000-000000000001',
            '10000000-0000-0000-0000-000000000002',
            '20000000-0000-0000-0000-000000000001',
            '2030-01-05T03:00:00Z',
            '2030-01-05T04:00:00Z',
            2
        );
        RAISE EXCEPTION 'Expected exclusion_violation was not raised';
    EXCEPTION
        WHEN exclusion_violation THEN
            RAISE NOTICE 'PASS: overlapping sale/property/vehicle booking was rejected';
    END;

    BEGIN
        UPDATE appointments
        SET starts_at = '2030-01-05T02:45:00Z'
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
