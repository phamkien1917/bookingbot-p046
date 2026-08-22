BEGIN;

ALTER TABLE sale_profiles
    ADD COLUMN IF NOT EXISTS calendar_access_token TEXT,
    ADD COLUMN IF NOT EXISTS calendar_refresh_token TEXT,
    ADD COLUMN IF NOT EXISTS calendar_token_expires_at TIMESTAMPTZ;

UPDATE property_media
SET url = 'https://www.nerahome.space/property-placeholder.svg'
WHERE url IN (
    'https://images.example.com/sr-a1208-cover.jpg',
    'https://images.example.com/sr-l18-cover.jpg'
);

COMMIT;
