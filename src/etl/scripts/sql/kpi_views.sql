-- create kpi views

BEGIN;

-- 1. Total leave days per employee [leave_details]
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.total_leave_days_per_employee_mv AS
WITH ranked_leaves AS (
    SELECT
        ft.empId,
        ed.firstName,
        ed.lastName,
        EXTRACT(YEAR FROM fd.fiscal_start_date) AS fiscal_year,
        fd.fiscal_start_date,
        fd.fiscal_end_date,
        MAX(ft.defaultDays) AS default_days,
        MAX(ft.transferableDays) AS transferable_days,
        SUM(ft.leaveDays) AS total_leave_days,
        ROW_NUMBER() OVER (PARTITION BY fd.fiscal_start_date ORDER BY SUM(ft.leaveDays) DESC) AS rn
    FROM
        dw.fact_table ft
    INNER JOIN dw.employee_details ed ON ed.empId = ft.empId
    INNER JOIN dw.fiscal_detail fd ON fd.fiscal_id = ft.fiscalid
    GROUP BY ft.empId, ed.firstName, ed.lastName, fd.fiscal_start_date, fd.fiscal_end_date
)
SELECT
    empId,
    firstName,
    lastName,
    fiscal_year,
    fiscal_start_date,
    fiscal_end_date,
    default_days,
    transferable_days,
    total_leave_days
FROM
    ranked_leaves
WHERE
    rn <= 10 AND fiscal_year <> '2024';

CREATE UNIQUE INDEX IF NOT EXISTS idx_total_leave_days_per_employee_mv ON dw.total_leave_days_per_employee_mv (empId, firstName, lastName, fiscal_start_date, fiscal_end_date);

-- 2. Employee details [hr_details]
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.employee_details_mv AS
SELECT
    ft.empId,
    ed.firstName,
    ed.lastName,
    fd.fiscal_start_date,
    fd.fiscal_end_date,
    ed.designationname,
    al.name AS project_name
FROM
    dw.fact_table ft
INNER JOIN dw.employee_details ed ON ed.empId = ft.empId
INNER JOIN dw.allocations al ON al.empid = ed.empid
INNER JOIN dw.fiscal_detail fd ON fd.fiscal_id = ft.fiscalid
GROUP BY
    ft.empId, ed.firstName, ed.lastName, ed.designationname, al.name, fd.fiscal_start_date, fd.fiscal_end_date;

CREATE UNIQUE INDEX IF NOT EXISTS idx_employee_details_mv ON dw.employee_details_mv (empId, firstName, lastName, designationname, project_name, fiscal_start_date, fiscal_end_date);

-- 3. Leave trends by month [trends: Month]
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_trends_by_month_mv AS
SELECT
    EXTRACT(MONTH FROM startDate) AS month,
    EXTRACT(YEAR FROM startDate) AS year,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
INNER JOIN dw.leave_type lt ON ft.leaveTypeId = lt.leave_type_id
GROUP BY month, year;

CREATE UNIQUE INDEX IF NOT EXISTS idx_leave_trends_by_month_mv ON dw.leave_trends_by_month_mv (year, month);

-- 4. Leave trend by fiscal year [trend : fiscal year]
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_trend_by_fiscal_year_per_leave_type_mv AS
SELECT
    fd.fiscal_id,
    fd.fiscal_start_date,
    fd.fiscal_end_date,
    lt.leavetypename,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
JOIN
    dw.fiscal_detail fd ON ft.fiscalId = fd.fiscal_id
JOIN
    dw.leave_type lt ON lt.leave_type_id = ft.leavetypeid
GROUP BY
    fd.fiscal_id, fd.fiscal_start_date, fd.fiscal_end_date, lt.leavetypename
ORDER BY
    fd.fiscal_id;

-- 5. Leave trend by fiscal year per department
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_request_distribution_by_department_and_leave_types_mv AS
SELECT
    fd.fiscal_start_date,
    fd.fiscal_end_date,
    ed.departmentDescription,
    lt.leaveTypeName,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
JOIN dw.fiscal_detail fd ON ft.fiscalId = fd.fiscal_id
JOIN dw.employee_details ed ON ft.empId = ed.empId
JOIN dw.leave_type lt ON ft.leaveTypeId = lt.leave_type_id
GROUP BY ed.departmentDescription, lt.leaveTypeName, fd.fiscal_start_date, fd.fiscal_end_date ;


CREATE UNIQUE INDEX IF NOT EXISTS idx_leave_trend_by_fiscal_year_per_leave_type_mv
    ON dw.leave_trend_by_fiscal_year_per_leave_type_mv (fiscal_id, fiscal_start_date, fiscal_end_date, leavetypename);

-- 6. Top 10 project allocations
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.top_10_project_allocations_mv AS
SELECT
    name,
    COUNT(*) AS request_count
FROM
    dw.allocations
GROUP BY name
ORDER BY request_count DESC
LIMIT 10;

-- We cannot create a unique index on limited result set; skip index here or use a surrogate key if needed.

COMMIT;
