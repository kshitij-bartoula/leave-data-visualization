BEGIN;
-- Create user_accounts table
CREATE TABLE IF NOT EXISTS config.import_config (
    id SERIAL PRIMARY KEY,
    api_name TEXT NOT NULL,
    is_ingestion_enabled boolean NOT NULL UNIQUE,
    is_transformation_enabled boolean NOT NULL
);
commit;
