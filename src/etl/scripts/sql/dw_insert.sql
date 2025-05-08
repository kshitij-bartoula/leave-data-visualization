BEGIN;

-- employee_details: UPDATE then INSERT
UPDATE dw.employee_details AS ed
SET
    designationId = a.designation_id,
    designationName = a.designation_name,
    firstName = a.first_name,
    middleName = a.middle_name,
    lastName = a.last_name,
    email = a.email,
    departmentDescription = a.department_description
FROM (
    SELECT DISTINCT * FROM dbo.cleaned_api_data
) a
WHERE ed.empId = a.emp_id
  AND (
    ed.designationId IS DISTINCT FROM a.designation_id OR
    ed.designationName IS DISTINCT FROM a.designation_name OR
    ed.firstName IS DISTINCT FROM a.first_name OR
    ed.middleName IS DISTINCT FROM a.middle_name OR
    ed.lastName IS DISTINCT FROM a.last_name OR
    ed.email IS DISTINCT FROM a.email OR
    ed.departmentDescription IS DISTINCT FROM a.department_description
);

INSERT INTO dw.employee_details (
    empId, designationId, designationName,
    firstName, middleName, lastName, email, departmentDescription
)
SELECT DISTINCT
    emp_id, designation_id, designation_name,
    first_name, middle_name, last_name, email, department_description
FROM dbo.cleaned_api_data a
WHERE NOT EXISTS (
    SELECT 1 FROM dw.employee_details ed WHERE ed.empId = a.emp_id
);

-- allocations: UPDATE then INSERT
UPDATE dw.allocations AS d
SET
    name = a.name,
    type = a.type
FROM (
    SELECT DISTINCT * FROM dbo.cleaned_allocations
) a
WHERE d.id = a.id AND d.empId = a.emp_id
  AND (
    d.name IS DISTINCT FROM a.name OR
    d.type IS DISTINCT FROM a.type
);

INSERT INTO dw.allocations (id, empId, name, type)
SELECT DISTINCT id, emp_id, name, type
FROM dbo.cleaned_allocations a
WHERE NOT EXISTS (
    SELECT 1 FROM dw.allocations d WHERE d.id = a.id AND d.empId = a.emp_id
);

-- leave_type: UPDATE then INSERT
UPDATE dw.leave_type AS lt
SET leavetypename = a.leave_type
FROM (
    SELECT DISTINCT leave_type_id, leave_type FROM dbo.cleaned_api_data
) a
WHERE lt.leave_type_id = a.leave_type_id
  AND lt.leavetypename IS DISTINCT FROM a.leave_type;

INSERT INTO dw.leave_type (leave_type_id, leavetypename)
SELECT DISTINCT leave_type_id, leave_type
FROM dbo.cleaned_api_data a
WHERE NOT EXISTS (
    SELECT 1 FROM dw.leave_type lt WHERE lt.leave_type_id = a.leave_type_id
);

-- fiscal_detail: UPDATE then INSERT
UPDATE dw.fiscal_detail AS fd
SET fiscal_start_date = a.fiscal_start_date::date,
    fiscal_end_date = a.fiscal_end_date::date
FROM (
    SELECT DISTINCT fiscal_id, fiscal_start_date, fiscal_end_date
    FROM dbo.cleaned_api_data
) a
WHERE fd.fiscal_id = a.fiscal_id
  AND (
    fd.fiscal_start_date IS DISTINCT FROM a.fiscal_start_date::date OR
    fd.fiscal_end_date IS DISTINCT FROM a.fiscal_end_date::date
);

INSERT INTO dw.fiscal_detail (fiscal_id, fiscal_start_date, fiscal_end_date)
SELECT DISTINCT fiscal_id, fiscal_start_date::date, fiscal_end_date::date
FROM dbo.cleaned_api_data a
WHERE NOT EXISTS (
    SELECT 1 FROM dw.fiscal_detail fd WHERE fd.fiscal_id = a.fiscal_id
);

-- fact_table: UPDATE then INSERT
UPDATE dw.fact_table AS f
SET
    userId = a.user_id,
    teamManagerId = a.team_manager_id,
    isHr = a.is_hr,
    isSupervisor = a.is_supervisor,
    startDate = a.start_date::date,
    endDate = a.end_date::date,
    leaveDays = a.leave_days,
    reason = a.reason,
    status = a.status,
    leaveTypeId = a.leave_type_id,
    defaultDays = a.default_days,
    transferableDays = a.transferable_days,
    isConsecutive = CASE WHEN a.is_consecutive THEN 1 ELSE 0 END,
    fiscalId = a.fiscal_id,
    fiscalIsCurrent = a.fiscal_is_current,
    isConverted = CASE WHEN a.is_converted THEN 1 ELSE 0 END,
    createdAt = a.created_at,
    updatedAt = a.updated_at
FROM (
    SELECT DISTINCT * FROM dbo.cleaned_api_data
) a
WHERE f.id = a.id AND f.empId = a.emp_id;

INSERT INTO dw.fact_table (
    id, userId, empId, teamManagerId,
    isHr, isSupervisor, startDate, endDate,
    leaveDays, reason, status, leaveTypeId,
    defaultDays, transferableDays, isConsecutive,
    fiscalId, fiscalIsCurrent, isConverted,
    createdAt, updatedAt
)
SELECT DISTINCT
    id, user_id, emp_id, team_manager_id,
    is_hr, is_supervisor, start_date::date, end_date::date,
    leave_days, reason, status, leave_type_id,
    default_days, transferable_days,
    CASE WHEN is_consecutive THEN 1 ELSE 0 END,
    fiscal_id, fiscal_is_current,
    CASE WHEN is_converted THEN 1 ELSE 0 END,
    created_at, updated_at
FROM dbo.cleaned_api_data a
WHERE NOT EXISTS (
    SELECT 1 FROM dw.fact_table f WHERE f.id = a.id AND f.empId = a.emp_id
);

COMMIT;


