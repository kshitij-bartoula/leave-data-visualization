BEGIN;

INSERT INTO dw.employee_details AS ed
SELECT
    a."empId"::int,
    a."designationId",
    a."designationName",
    a."firstName",
    a."middleName",
    a."lastName",
    a."email",
    a."departmentDescription"
FROM (
    SELECT DISTINCT
        "empId"::int,
        "designationId",
        "designationName",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "departmentDescription"
    FROM raw.api_data
) a
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.employee_details ed
    WHERE ed.empId = a."empId"::int
);

UPDATE dw.employee_details AS ed
SET
    designationId = a."designationId",
    designationName = a."designationName",
    firstName = a."firstName",
    middleName = a."middleName",
    lastName = a."lastName",
    email = a."email",
    departmentDescription = a."departmentDescription"
FROM (
    SELECT
        "empId"::int,
        "designationId",
        "designationName",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "departmentDescription"
    FROM raw.api_data
) a
WHERE ed.empId = a."empId"::int
AND (
    ed.designationId <> a."designationId"
    OR ed.designationName <> a."designationName"
    OR ed.email <> a."email"
    OR ed.departmentDescription <> a."departmentDescription"
);

INSERT INTO dw.allocations
SELECT
    a."empId"::int,
    a."id",
    a."name",
    a."type"
FROM (
    SELECT DISTINCT
        "empId",
        "id",
        "name",
        "type"
    FROM raw.allocation_data
) a
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.allocations alloc
    WHERE alloc.empId::int = a."empId"::int
    AND alloc.id = a."id"
);

INSERT INTO dw.leave_type
SELECT
    a."leaveTypeId"::int,
    a."leaveType"
FROM (
    SELECT DISTINCT
        "leaveTypeId",
        "leaveType"
    FROM raw.api_data
) a
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.leave_type lt
    WHERE lt.leave_type_id::int = a."leaveTypeId"::int
    AND lt.leavetypename = a."leaveType"
);

--for fiscal_detail
INSERT INTO dw.fiscal_detail
SELECT
    a."fiscalId"::int,
    a."fiscalStartDate"::timestamp with time zone,
    a."fiscalEndDate"::timestamp with time zone
FROM (
    SELECT DISTINCT
        "fiscalId",
        "fiscalStartDate",
        "fiscalEndDate"
    FROM raw.api_data
) a
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.fiscal_detail fd
    WHERE fd.fiscal_id::int = a."fiscalId"::int
);


INSERT INTO dw.fact_table
SELECT
    a."id",
    a."userId",
    a."empId"::int,
    a."teamManagerId",
    a."isHr",
    a."isSupervisor",
    a."startDate"::date,
    a."endDate"::date,
    a."leaveDays"::int,
    a."reason",
    a."status",
    a."leaveTypeId",
    a."defaultDays"::int,
    a."transferableDays"::int,
    a."isConsecutive"::int,
    a."fiscalId",
    a."fiscalIsCurrent",
    a."isConverted"::int,
    a."createdAt"::timestamp,
    a."updatedAt"::timestamp
FROM (
    SELECT DISTINCT
        "id",
        "userId",
        "empId",
        "teamManagerId",
        "isHr",
        "isSupervisor",
        "startDate",
        "endDate",
        "leaveDays",
        "reason",
        "status",
        "leaveTypeId",
        "defaultDays",
        "transferableDays",
        "isConsecutive",
        "fiscalId",
        "fiscalIsCurrent",
        "isConverted",
        "createdAt",
        "updatedAt"
    FROM raw.api_data
) a
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.fact_table fact
    WHERE fact.id = a."id"
    AND fact.empId::int = a."empId"::int
    AND fact.status = a."status"
);

COMMIT;
