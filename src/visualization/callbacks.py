# visualization/callbacks.py
from dash.dependencies import Input, Output
from data_processing import (
    employee_leave, leave_balance, leave_trend, leave_distribution,
    leave_trend_fiscal_year, department_leave_distribution, leave_reason
)
from components import (
    gen_employee_leave, gen_leave_balance, gen_leave_trend, gen_leave_distribution,
    gen_leave_trend_fiscal_year, gen_department_leave_distribution, gen_leave_reason,
    gen_employee_leave_filter_options, gen_leave_balance_filter_options,
    gen_leave_trend_filter_options, gen_leave_distribution_filter_options,
    gen_leave_trend_fiscal_year_filter_options, gen_department_leave_distribution_filter_options,
    gen_leave_reason_filter_options
)
from endpoints import (
    ENDPOINT_EMPLOYEE_LEAVE, ENDPOINT_LEAVE_BALANCE, ENDPOINT_LEAVE_TREND,
    ENDPOINT_LEAVE_DISTRIBUTION, ENDPOINT_LEAVE_TREND_FISCAL_YEAR,
    ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION, ENDPOINT_LEAVE_REASONS
)

def register_callbacks(app):
    @app.callback(
        Output('data-chart', 'figure'),
        [Input('filter-dropdown', 'value'),
         Input('filter-value-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_chart(selected_filter, selected_value, n_intervals):
        if selected_filter == 'employee_leave':
            data = employee_leave(ENDPOINT_EMPLOYEE_LEAVE)
            figure = gen_employee_leave(data, selected_value)
        elif selected_filter == 'leave_balance':
            data = leave_balance(ENDPOINT_LEAVE_BALANCE)
            figure = gen_leave_balance(data, selected_value)
        elif selected_filter == 'leave_trend':
            data = leave_trend(ENDPOINT_LEAVE_TREND)
            figure = gen_leave_trend(data, selected_value)
        elif selected_filter == 'leave_distribution':
            data = leave_distribution(ENDPOINT_LEAVE_DISTRIBUTION)
            figure = gen_leave_distribution(data, selected_value)
        elif selected_filter == 'leave_trend_fiscal_year':
            data = leave_trend_fiscal_year(ENDPOINT_LEAVE_TREND_FISCAL_YEAR)
            figure = gen_leave_trend_fiscal_year(data, selected_value)
        elif selected_filter == 'department_leave_distribution':
            data = department_leave_distribution(ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION)
            figure = gen_department_leave_distribution(data, selected_value)
        elif selected_filter == 'leave_reason':
            data = leave_reason(ENDPOINT_LEAVE_REASONS)
            figure = gen_leave_reason(data, selected_value)
        return figure

    @app.callback(
        Output('filter-value-dropdown', 'options'),
        [Input('filter-dropdown', 'value')]
    )
    def update_filter_options(selected_filter):
        if selected_filter == 'employee_leave':
            data = employee_leave(ENDPOINT_EMPLOYEE_LEAVE)
            options = gen_employee_leave_filter_options(data)
        elif selected_filter == 'leave_balance':
            data = leave_balance(ENDPOINT_LEAVE_BALANCE)
            options = gen_leave_balance_filter_options(data)
        elif selected_filter == 'leave_trend':
            data = leave_trend(ENDPOINT_LEAVE_TREND)
            options = gen_leave_trend_filter_options(data)
        elif selected_filter == 'leave_distribution':
            data = leave_distribution(ENDPOINT_LEAVE_DISTRIBUTION)
            options = gen_leave_distribution_filter_options(data)
        elif selected_filter == 'leave_trend_fiscal_year':
            data = leave_trend_fiscal_year(ENDPOINT_LEAVE_TREND_FISCAL_YEAR)
            options = gen_leave_trend_fiscal_year_filter_options(data)
        elif selected_filter == 'department_leave_distribution':
            data = department_leave_distribution(ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION)
            options = gen_department_leave_distribution_filter_options(data)
        elif selected_filter == 'leave_reason':
            data = leave_reason(ENDPOINT_LEAVE_REASONS)
            options = gen_leave_reason_filter_options(data)
        return options

# Import at the end to avoid circular import
from app import app
register_callbacks(app)
