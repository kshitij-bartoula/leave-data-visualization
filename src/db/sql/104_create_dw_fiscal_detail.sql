BEGIN;

CREATE TABLE IF NOT EXISTS dw.fiscal_detail (
    fiscal_id INT PRIMARY KEY,
    fiscal_start_date DATE,
    fiscal_end_date DATE
);

COMMIT;
