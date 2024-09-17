BEGIN;

CREATE TABLE IF NOT EXISTS dw.leave_type (
    leave_type_id INT PRIMARY KEY,
    leavetypename varchar(255)
);

COMMIT;
