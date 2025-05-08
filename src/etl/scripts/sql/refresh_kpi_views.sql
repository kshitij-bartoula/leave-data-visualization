-- refresh_kpi_views.py

BEGIN;

-- Refresh materialized views concurrently
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.total_leave_days_per_employee_mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.employee_details_mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.leave_trends_by_month_mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.leave_distribution_by_leave_type_mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.leave_trend_by_fiscal_year_per_leave_type_mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.leave_request_distribution_by_department_and_leave_types_mv;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY dw.leave_status_count_by_department_mv;
REFRESH MATERIALIZED VIEW dw.top_10_project_allocations_mv;

COMMIT;
