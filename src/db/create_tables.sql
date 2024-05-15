BEGIN;
CREATE TABLE IF NOT EXISTS employee_details (
    empId INT PRIMARY KEY,
    designationId INT,
    designationName VARCHAR(255),
    firstName VARCHAR(255),
    middleName VARCHAR(255),
    lastName VARCHAR(255),
    email VARCHAR(255),
    departmentDescription VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS leave_type (
    leave_type_id INT PRIMARY KEY,
    leavetypename varchar(255)
);

CREATE TABLE IF NOT EXISTS fiscal_detail (
    fiscal_id INT PRIMARY KEY,
    fiscal_start_date TIMESTAMP WITH TIME ZONE,
    fiscal_end_date TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS allocations (
    empId INT,
    id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    CONSTRAINT fk_employee_details_empid FOREIGN KEY (empId) REFERENCES employee_details(empId)
);

CREATE TABLE IF NOT EXISTS fact_table (
    id INT,
    userId INT,
    empId INT,
    teamManagerId INT,
    isHr BOOL,
    isSupervisor BOOL,
    startDate DATE,
    endDate DATE,
    leaveDays INT,
    reason text,
    status varchar(255),
    remarks text,
    leaveTypeId INT,
    defaultDays INT,
    transferableDays INT,
    isConsecutive INT,
    fiscalId INT,
    fiscalIsCurrent BOOL,
    isConverted INT,
    createdAt TIMESTAMP WITH TIME ZONE,
    updatedAt TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_empId_employee_details FOREIGN KEY (empId) REFERENCES employee_details(empId),
    CONSTRAINT fk_leave_type FOREIGN KEY (leaveTypeId) REFERENCES leave_type(leave_type_id),
    CONSTRAINT fk_fiscall_detail FOREIGN KEY (fiscalId) REFERENCES fiscal_detail (fiscal_id)
);

COMMIT;
