Begin;

TRUNCATE TABLE dbo.cleaned_allocations;

INSERT INTO dbo.cleaned_allocations (
    id, emp_id, name, type
)
SELECT
    id,
    cast("empId" as int),
    name,
    type
FROM raw.allocation_data
WHERE
    "empId" IS NOT NULL
    AND name IS NOT NULL
    AND type IS NOT NULL;

TRUNCATE TABLE dbo.cleaned_api_data;

INSERT INTO dbo.cleaned_api_data (
    id, user_id, emp_id, team_manager_id, designation_id,
    designation_name, first_name, middle_name, last_name, email,
    is_hr, is_supervisor, leave_issuer_id, issuer_first_name,
    issuer_middle_name, issuer_last_name, current_leave_issuer_id,
    current_leave_issuer_email, department_description, start_date,
    end_date, leave_days, reason, leave_status, status,
    response_remarks, leave_type_id, leave_type, default_days,
    transferable_days, is_consecutive, fiscal_id, fiscal_start_date,
    fiscal_end_date, fiscal_is_current, created_at, updated_at,
    is_automated, is_converted, total_count, allocations
)
SELECT
    id,
    "userId",
    cast("empId" as int),
    "teamManagerId",
    "designationId",
    "designationName",
    "firstName",
    "middleName",
    "lastName",
    email,
    "isHr",
    "isSupervisor",
    "leaveIssuerId",
    "issuerFirstName",
    "issuerMiddleName",
    "issuerLastName",
    "currentLeaveIssuerId",
    "currentLeaveIssuerEmail",
    "departmentDescription",
    TO_TIMESTAMP("startDate", 'YYYY-MM-DD"T"HH24:MI:SS'),  -- adjust format if needed
    TO_TIMESTAMP("endDate", 'YYYY-MM-DD"T"HH24:MI:SS'),
    "leaveDays",
    reason,
    "leaveStatus",
    status,
    "responseRemarks",
    "leaveTypeId",
    "leaveType",
    "defaultDays",
    "transferableDays",
    CASE WHEN "isConsecutive" = 1 THEN TRUE ELSE FALSE END,
    "fiscalId",
    TO_TIMESTAMP("fiscalStartDate", 'YYYY-MM-DD"T"HH24:MI:SS'),
    TO_TIMESTAMP("fiscalEndDate", 'YYYY-MM-DD"T"HH24:MI:SS'),
    "fiscalIsCurrent",
    TO_TIMESTAMP("createdAt", 'YYYY-MM-DD"T"HH24:MI:SS'),
    TO_TIMESTAMP("updatedAt", 'YYYY-MM-DD"T"HH24:MI:SS'),
    CASE WHEN "isAutomated" = 1 THEN TRUE ELSE FALSE END,
    CASE WHEN "isConverted" = 1 THEN TRUE ELSE FALSE END,
    "totalCount",
    allocations
FROM raw.api_data
WHERE
    "empId" IS NOT NULL
    AND "startDate" IS NOT NULL
    AND "endDate" IS NOT NULL
    AND email IS NOT NULL;

commit;
