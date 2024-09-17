BEGIN;

CREATE TABLE IF NOT EXISTS dw.fact_table (
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
    leaveTypeId INT,
    defaultDays INT,
    transferableDays INT,
    isConsecutive INT,
    fiscalId INT,
    fiscalIsCurrent BOOL,
    isConverted INT,
    createdAt TIMESTAMP WITH TIME ZONE,
    updatedAt TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_empId_employee_details FOREIGN KEY (empId) REFERENCES dw.employee_details(empId),
    CONSTRAINT fk_leave_type FOREIGN KEY (leaveTypeId) REFERENCES dw.leave_type(leave_type_id),
    CONSTRAINT fk_fiscall_detail FOREIGN KEY (fiscalId) REFERENCES dw.fiscal_detail (fiscal_id)
);

COMMIT;
