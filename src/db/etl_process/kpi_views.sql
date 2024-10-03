--- create kpi views

BEGIN;

--1. Total leave days per employee (approved)
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.total_leave_days_per_employee_mv AS
SELECT
    ft.empId,
    ed.firstName,
    ed.lastName,
    SUM(ft.leaveDays) AS total_leave_days
FROM
    dw.fact_table ft
INNER JOIN
    dw.employee_details ed ON ed.empId = ft.empId
GROUP BY
    ft.empId, ed.firstName, ed.lastName;


CREATE MATERIALIZED VIEW IF NOT EXISTS dw.employee_details_mv AS
SELECT
    ft.empId,
    ed.firstName,
    ed.lastName,
    cast(fd.fiscal_start_date as date),
    cast(fd.fiscal_end_date as date),
    ed.designationname,
    al.name as project_name
FROM
    dw.fact_table ft
INNER JOIN
    dw.employee_details ed ON ed.empId = ft.empId
INNER JOIN
    dw.allocations al ON al.empid = ed.empid
inner join
    dw.fiscal_detail fd on fd.fiscal_id = ft.fiscalid
GROUP BY
    ft.empId, ed.firstName, ed.lastName,ed.designationname,al.name,fd.fiscal_start_date,fd.fiscal_end_date;

-- Leave balances per employee (approved)
-- CREATE MATERIALIZED VIEW IF NOT EXISTS leave_balances_per_employee_mv AS
-- SELECT
--     ft.empId,
--     ed.firstName,
--     ed.lastName,
--     MAX(ft.defaultDays) AS defaultDays,
--     MAX(ft.transferabledays) AS transferabledays,
--     SUM(ft.leaveDays) AS leaveDays,
--     MAX(ft.defaultDays) + MAX(ft.transferabledays) - SUM(ft.leaveDays) AS leave_balance
-- FROM
--     dw.fact_table ft
-- INNER JOIN
--     dw.employee_details ed ON ed.empId = ft.empId
-- GROUP BY
--     ft.empId, ed.firstName, ed.lastName;

-- Leave trends by month (approved)
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_trends_by_month_mv AS
SELECT
    EXTRACT(MONTH FROM startDate) AS month,
    EXTRACT(YEAR FROM startDate) AS year,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
INNER JOIN
    dw.leave_type lt ON ft.leaveTypeId = lt.leave_type_id
GROUP BY
    month, year
ORDER BY
    year ASC, month ASC;

-- Leave distribution by leave type
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_distribution_by_leave_type_mv AS
SELECT
    lt.leavetypename,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
JOIN
    dw.leave_type lt ON ft.leaveTypeId = lt.leave_type_id
GROUP BY
    lt.leavetypename;

-- Leave trend by fiscal year per leave type
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

-- Leave request distribution as per department and leave types
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_request_distribution_by_department_and_leave_types_mv AS
SELECT
    ed.departmentDescription,
    lt.leaveTypeName,
    COUNT(*) AS leave_count
FROM
    dw.fact_table ft
JOIN
    dw.employee_details ed ON ft.empId = ed.empId
JOIN
    dw.leave_type lt ON ft.leaveTypeId = lt.leave_type_id
GROUP BY
    ed.departmentDescription,
    lt.leaveTypeName;

-- -- Leave status count by department
-- CREATE MATERIALIZED VIEW IF NOT EXISTS dw.leave_status_count_by_department_mv AS
-- SELECT
--     ed.departmentDescription,
--     COUNT(CASE WHEN ft.status = 'APPROVED' THEN 1 END) AS approved,
--     COUNT(CASE WHEN ft.status = 'REJECTED' THEN 1 END) AS rejected,
--     COUNT(CASE WHEN ft.status = 'REQUESTED' THEN 1 END) AS requested,
--     COUNT(CASE WHEN ft.status = 'CANCELLED' THEN 1 END) AS cancelled
-- FROM
--     dw.fact_table ft
-- JOIN
--     dw.employee_details ed ON ft.empId = ed.empId
-- GROUP BY
--     ed.departmentDescription;

-- TOP 10 project allocations
CREATE MATERIALIZED VIEW IF NOT EXISTS dw.top_10_project_allocations_mv AS
SELECT
    name,
    COUNT(*) AS request_count
FROM
    dw.allocations
GROUP BY
    name
ORDER BY
    request_count DESC
LIMIT 10;

COMMIT;
