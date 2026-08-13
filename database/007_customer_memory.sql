-- Persistent conversational preferences used to personalize future searches.
CREATE TABLE IF NOT EXISTS customer_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_user_id UUID NOT NULL REFERENCES customer_profiles(user_id) ON DELETE CASCADE,
    preference_key VARCHAR(100) NOT NULL,
    preference_value JSONB NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL DEFAULT 1.0,
    source VARCHAR(20) NOT NULL DEFAULT 'EXPLICIT',
    last_confirmed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_customer_preferences_key UNIQUE (customer_user_id, preference_key)
);

CREATE INDEX IF NOT EXISTS ix_customer_preferences_customer
    ON customer_preferences (customer_user_id, updated_at DESC);

DROP TRIGGER IF EXISTS trg_customer_preferences_updated_at ON customer_preferences;
CREATE TRIGGER trg_customer_preferences_updated_at
BEFORE UPDATE ON customer_preferences
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
