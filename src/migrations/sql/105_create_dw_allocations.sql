BEGIN;

    CREATE TABLE IF NOT EXISTS dw.allocations (
        id INT,
        empId INT,
        name VARCHAR(255),
        type VARCHAR(255),
        CONSTRAINT fk_employee_details_empid FOREIGN KEY (empId) REFERENCES dw.employee_details(empId)
    );

COMMIT;
