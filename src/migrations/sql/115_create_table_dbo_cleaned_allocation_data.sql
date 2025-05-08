
BEGIN;

    CREATE TABLE IF NOT EXISTS dbo.cleaned_allocations (
        id INT,
        emp_id INT,
        name VARCHAR(255),
        type VARCHAR(255)
    );

COMMIT;