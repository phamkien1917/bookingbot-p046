-- Persistent customer favorites. Safe to run after database/005_batdongsan_data.sql.
CREATE TABLE IF NOT EXISTS saved_properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_saved_properties_customer_property UNIQUE (customer_user_id, property_id)
);

CREATE INDEX IF NOT EXISTS ix_saved_properties_customer
    ON saved_properties (customer_user_id, created_at DESC);

DROP TRIGGER IF EXISTS trg_saved_properties_updated_at ON saved_properties;
CREATE TRIGGER trg_saved_properties_updated_at
BEFORE UPDATE ON saved_properties
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
