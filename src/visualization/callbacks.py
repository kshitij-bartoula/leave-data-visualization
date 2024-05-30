from dash.dependencies import Output, Input
import plotly.graph_objs as go
from data_processing import (
    employee_leave, leave_trend, leave_distribution,
    leave_trend_fiscal_year, department_leave_distribution, leave_reason
)
from components import (
    gen_employee_leave, gen_leave_trend, gen_leave_distribution,
    gen_leave_trend_fiscal_year, gen_department_leave_distribution, gen_leave_reason
)
from endpoints import (
    ENDPOINT_EMPLOYEE_LEAVE, ENDPOINT_LEAVE_TREND,
    ENDPOINT_LEAVE_DISTRIBUTION, ENDPOINT_LEAVE_TREND_FISCAL_YEAR,
    ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION, ENDPOINT_LEAVE_REASONS
)

def register_callbacks(app):
    @app.callback(
        Output('leave-trend-graph', 'figure'),
        Output('leave-distribution-graph', 'figure'),
        Output('leave-trend-fiscal-year-graph', 'figure'),
        Output('department-leave-distribution-graph', 'figure'),
        Output('leave-reason-graph', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_chart(n_intervals):

        data_leave_trend = leave_trend(ENDPOINT_LEAVE_TREND)
        figure_leave_trend = gen_leave_trend(data_leave_trend)

        data_leave_distribution = leave_distribution(ENDPOINT_LEAVE_DISTRIBUTION)
        figure_leave_distribution = gen_leave_distribution(data_leave_distribution)

        data_leave_trend_fiscal_year = leave_trend_fiscal_year(ENDPOINT_LEAVE_TREND_FISCAL_YEAR)
        figure_leave_trend_fiscal_year = gen_leave_trend_fiscal_year(data_leave_trend_fiscal_year)

        data_department_leave_distribution = department_leave_distribution(ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION)
        figure_department_leave_distribution = gen_department_leave_distribution(data_department_leave_distribution)

        data_leave_reason = leave_reason(ENDPOINT_LEAVE_REASONS)
        figure_leave_reason = gen_leave_reason(data_leave_reason)

        return (
            figure_leave_trend,
            figure_leave_distribution,
            figure_leave_trend_fiscal_year,
            figure_department_leave_distribution,
            figure_leave_reason
        )

    @app.callback(
        [Output('employee-leave-graph', 'figure'),
        Output('employee-dropdown', 'options')],
        [Input('employee-dropdown', 'value'),
        Input('employee-dropdown', 'search_value')]
    )
    def update_employee_leave(selected_employee, search_value):
        # Retrieve data for all employees
        data_employee_leave = employee_leave(ENDPOINT_EMPLOYEE_LEAVE)

        # Filter data based on selected employee, if any
        if selected_employee:
            data_employee_leave = [entry for entry in data_employee_leave if selected_employee in (entry['firstName'] + ' ' + entry['lastName'])]

        # Generate figure based on filtered data
        figure_employee_leave = gen_employee_leave(data_employee_leave)

        # Create dropdown options with employee full names
        employee_names = [{'label': f"{entry['firstName']} {entry['lastName']}", 'value': f"{entry['firstName']} {entry['lastName']}"} for entry in data_employee_leave]

        # Filter options based on user input if search_value is provided
        if search_value:
            employee_names = [employee for employee in employee_names if search_value.lower() in employee['label'].lower()]

        return figure_employee_leave, employee_names

