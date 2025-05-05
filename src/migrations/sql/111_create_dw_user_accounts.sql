BEGIN;
-- Create user_accounts table
CREATE TABLE IF NOT EXISTS dw.user_accounts (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
commit;