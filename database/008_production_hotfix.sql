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

DELETE FROM property_external_sellers WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM property_media WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM property_sale_assignments WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM tour_requests WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM appointments WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM property_holds WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM saved_properties WHERE property_id IN (SELECT id FROM properties WHERE code = 'BDS_PR46136708');
DELETE FROM properties WHERE code = 'BDS_PR46136708';

COMMIT;
