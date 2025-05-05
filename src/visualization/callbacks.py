from dash.dependencies import Output, Input
import plotly.graph_objs as go
from data_processing import fetch_data_from_api
# from data_processing import (
#     employee_leave, leave_trend, leave_distribution, employee_details,
#     leave_trend_fiscal_year, department_leave_distribution, project_allocations
# )
from components import (
    gen_employee_leave, gen_leave_trend, gen_leave_distribution, gen_employee_details,
    gen_leave_trend_fiscal_year, gen_department_leave_distribution, gen_project_allocations
)
from endpoints import (
    ENDPOINT_EMPLOYEE_LEAVE_DETAILS, ENDPOINT_LEAVE_TREND, ENDPOINT_EMPLOYEE_HR_DETAILS,
    ENDPOINT_LEAVE_DISTRIBUTION, ENDPOINT_LEAVE_TREND_FISCAL_YEAR,
    ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION, ENDPOINT_PROJECT_ALLOCATIONS
)

def register_callbacks(app):
    @app.callback(
        Output('leave-trend-graph', 'figure'),
        Output('leave-distribution-graph', 'figure'),
        Output('leave-trend-fiscal-year-graph', 'figure'),
        Output('department-leave-distribution-graph', 'figure'),
        Output('project-allocations-graph', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_chart(n_intervals):
        data_leave_trend = fetch_data_from_api(ENDPOINT_LEAVE_TREND)
        figure_leave_trend = gen_leave_trend(data_leave_trend)

        data_leave_distribution = fetch_data_from_api(ENDPOINT_LEAVE_DISTRIBUTION)
        figure_leave_distribution = gen_leave_distribution(data_leave_distribution)

        data_leave_trend_fiscal_year = fetch_data_from_api(ENDPOINT_LEAVE_TREND_FISCAL_YEAR)
        figure_leave_trend_fiscal_year = gen_leave_trend_fiscal_year(data_leave_trend_fiscal_year)

        data_department_leave_distribution = fetch_data_from_api(ENDPOINT_DEPARTMENT_LEAVE_DISTRIBUTION)
        figure_department_leave_distribution = gen_department_leave_distribution(data_department_leave_distribution)

        data_project_allocation = fetch_data_from_api(ENDPOINT_PROJECT_ALLOCATIONS)
        figure_project_allocations = gen_project_allocations(data_project_allocation)

        return (
            figure_leave_trend,
            figure_leave_distribution,
            figure_leave_trend_fiscal_year,
            figure_department_leave_distribution,
            figure_project_allocations
        )

    @app.callback(
        Output('project-dropdown', 'options'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_project_dropdown(n_intervals):
        data_projects = fetch_data_from_api(ENDPOINT_PROJECT_ALLOCATIONS)
        options = [{'label': project['name'], 'value': project['name']} for project in data_projects]
        return options

    @app.callback(
        Output('employee-leave-dropdown', 'options'),
        Output('employee-details-dropdown', 'options'),  # Update employee details dropdown as well
        [Input('interval-component', 'n_intervals')]
    )
    def update_employee_dropdown(n_intervals):
        data_employee = fetch_data_from_api(ENDPOINT_EMPLOYEE_HR_DETAILS)
        options = [{'label': f"{entry['firstName']} {entry['lastName']}", 'value': f"{entry['firstName']} {entry['lastName']}"} for entry in data_employee]
        return options, options  # Return for both dropdowns

    @app.callback(
        Output('employee-leave-table', 'data'),
        [Input('employee-leave-dropdown', 'value')]
    )
    def update_employee_leave(selected_employee):
        # Retrieve data for all employees
        data_employee_leave = fetch_data_from_api(ENDPOINT_EMPLOYEE_LEAVE_DETAILS)

        # Filter data based on selected employee, if any
        if selected_employee:
            data_employee_leave = [entry for entry in data_employee_leave if selected_employee in (entry['firstName'] + ' ' + entry['lastName'])]

        return data_employee_leave

    @app.callback(
        Output('employee-details-table', 'data'),
        [Input('employee-details-dropdown', 'value'),  # Employee dropdown
         Input('project-dropdown', 'value')]  # Project dropdown
    )
    def update_employee_details(selected_employee, selected_project):
        # Retrieve data for all employees
        data_employee_details = fetch_data_from_api(ENDPOINT_EMPLOYEE_HR_DETAILS)

        # Filter employee details based on selected employee
        if selected_employee:
            data_employee_details = [entry for entry in data_employee_details if
                                     f"{entry['firstName']} {entry['lastName']}" == selected_employee]

        # Further filter by selected project if one is chosen
        if selected_project:
            data_employee_details = [entry for entry in data_employee_details if
                                     entry['project_allocation'] == selected_project]

        return data_employee_details
