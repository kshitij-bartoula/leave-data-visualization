CREATE TABLE IF NOT EXISTS dw.employee_details (
    empId INT PRIMARY KEY,
    designationId INT,
    designationName VARCHAR(255),
    firstName VARCHAR(255),
    middleName VARCHAR(255),
    lastName VARCHAR(255),
    email VARCHAR(255),
    departmentDescription VARCHAR(255)
);
