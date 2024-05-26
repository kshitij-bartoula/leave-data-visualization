
BEGIN;

REFRESH MATERIALIZED VIEW dw.total_leave_days_per_employee_mv;
REFRESH MATERIALIZED VIEW dw.leave_trends_by_month_mv;
REFRESH MATERIALIZED VIEW dw.leave_distribution_by_leave_type_mv;
REFRESH MATERIALIZED VIEW dw.leave_trend_by_fiscal_year_per_leave_type_mv;
REFRESH MATERIALIZED VIEW dw.leave_request_distribution_by_department_and_leave_types_mv;
REFRESH MATERIALIZED VIEW dw.leave_status_count_by_department_mv;
REFRESH MATERIALIZED VIEW dw.most_frequent_leave_request_reasons_mv;

COMMIT;
