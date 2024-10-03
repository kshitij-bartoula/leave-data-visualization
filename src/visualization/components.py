import plotly.graph_objs as go
from datetime import datetime

# General chart formats
def generate_bar_chart(x_values, y_values, title, x_title, y_title, orientation='h'):
    trace = go.Bar(x=x_values, y=y_values, orientation=orientation)
    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
        margin=dict(l=100, r=10, t=50, b=50)
    )
    return go.Figure(data=[trace], layout=layout)

def generate_line_chart(x_labels, y_values, title, x_title, y_title):
    trace = go.Scatter(x=x_labels, y=y_values, mode='lines+markers')
    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
        margin=dict(l=40, r=10, t=50, b=40)
    )
    return go.Figure(data=[trace], layout=layout)

## Line chart for trend
def gen_leave_trend(data, filter_value=None):
    filtered_data = [entry for entry in data if entry['year'] == filter_value] if filter_value else data
    sorted_data = sorted(filtered_data, key=lambda entry: (entry['year'], entry['month']))
    x_labels = [f"{entry['year']}-{entry['month']}" for entry in sorted_data]
    y_values = [entry['leave_count'] for entry in sorted_data]

    return generate_line_chart(x_labels, y_values, 'Leave Trend', 'Year-Month', 'Leave Count')

# Bar chart to analyze leave count according to leave type and fiscal year
def gen_leave_trend_fiscal_year(data, filter_value=None):
    filtered_data = [entry for entry in data if entry['leavetypename'] == filter_value] if filter_value else data
    start_dates = [
        entry['fiscal_start_date'] if isinstance(entry['fiscal_start_date'], datetime) else datetime.strptime(entry['fiscal_start_date'], '%Y-%m-%d').date()
        for entry in filtered_data
    ]
    leave_counts = [entry['leave_count'] for entry in filtered_data]
    leave_types = [entry['leavetypename'] for entry in filtered_data]

    fiscal_years = sorted(set(start.year for start in start_dates))
    unique_leave_types = sorted(set(leave_types))

    data_traces = [
        go.Bar(
            x=fiscal_years,
            y=[sum(leave_counts[i] for i in range(len(start_dates)) if start_dates[i].year == year and leave_types[i] == leave_type) for year in fiscal_years],
            name=leave_type
        )
        for leave_type in unique_leave_types
    ]

    layout = go.Layout(
        title='Leave Counts by Leave Type and Fiscal Year',
        xaxis=dict(
            title='Fiscal Year',
            tickvals=fiscal_years,
            ticktext=[str(year) for year in fiscal_years]  # Use year as text without decimals
        ),
        yaxis=dict(title='Leave Count'),
        barmode='stack',
        margin=dict(l=40, r=10, t=50, b=40)
    )

    return go.Figure(data=data_traces, layout=layout)

## Employee leave details plotted as dash table during visualization
def gen_employee_leave(data, filter_value=None, default_count=10):
    filtered_data = [entry for entry in data if filter_value in (entry['firstName'] + ' ' + entry['lastName'])] if filter_value else data[:default_count]
    return filtered_data

## Employee HR details plotted as dash table during visualization
def gen_employee_details(data, filter_value=None, default_count=10):
    filtered_data = [entry for entry in data if filter_value.lower() in (entry['firstName'].lower() + ' ' + entry['lastName'].lower())] if filter_value else data[:default_count]
    return filtered_data

## Department wise leave distribution plotted as bar chart
def gen_department_leave_distribution(data, filter_value=None):
    department_leave_counts = {}
    leave_types = set()

    for entry in data:
        department = entry["departmentDescription"]
        leave_type = entry["leaveTypeName"]
        leave_count = entry["leave_count"]
        leave_types.add(leave_type)

        if department not in department_leave_counts:
            department_leave_counts[department] = {}
        department_leave_counts[department][leave_type] = leave_count

    departments = list(department_leave_counts.keys())
    leave_types = {filter_value} if filter_value else leave_types  # Filter if provided

    data_traces = [
        go.Bar(
            name=leave_type,
            y=departments,
            x=[department_leave_counts[department].get(leave_type, 0) for department in departments],
            orientation='h'
        )
        for leave_type in leave_types
    ]

    layout = go.Layout(
        title='Leave Counts by Department and Type',
        xaxis=dict(title='Leave Count'),
        yaxis=dict(title='Department'),
        margin=dict(l=100, r=10, t=50, b=50)
    )

    return go.Figure(data=data_traces, layout=layout)

# Top 10 project allocations plotted in bar graph
def gen_project_allocations(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['name'] == filter_value]
    sorted_data = sorted(data, key=lambda entry: entry['request_count'], reverse=True)
    top_data = sorted_data[:10]
    top_project_allocations = [entry['name'] for entry in top_data]
    top_project_allocations_counts = [entry['request_count'] for entry in top_data]

    title = 'Top 10 Project Allocations'
    x_title = 'Project Name'
    y_title = 'Count'

    trace = go.Bar(x=top_project_allocations, y=top_project_allocations_counts)
    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
        margin=dict(l=100, r=10, t=50, b=50)
    )

    return go.Figure(data=[trace], layout=layout)

## Percentage according to leave type plotted in line chart
def gen_leave_distribution(data, filter_value=None):
    filtered_data = [entry for entry in data if entry['leavetypename'] == filter_value] if filter_value else data

    leave_types = [entry['leavetypename'] for entry in filtered_data]
    leave_counts = [entry['leave_count'] for entry in filtered_data]

    unique_leave_types = sorted(set(leave_types))
    leave_count_by_type = [sum(count for leave_type, count in zip(leave_types, leave_counts) if leave_type == lt) for lt in unique_leave_types]

    return generate_line_chart(unique_leave_types, leave_count_by_type, 'Leave Types Distribution', 'Leave Type', 'Leave Count')
