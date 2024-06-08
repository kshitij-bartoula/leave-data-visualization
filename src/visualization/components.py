# visualization/components.py
import plotly.graph_objs as go
from datetime import datetime

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

def generate_pie_chart(labels, values, title):
    trace = go.Pie(labels=labels, values=values)
    layout = go.Layout(
        title=title,
        margin=dict(l=40, r=10, t=50, b=40)
    )
    return go.Figure(data=[trace], layout=layout)

def gen_employee_leave(data, filter_value=None, default_count=10):
    if filter_value:
        filtered_data = [entry for entry in data if filter_value in (entry['firstName'] + ' ' + entry['lastName'])]
    else:
        filtered_data = data[:default_count]  # Show only the first `default_count` employees by default

    y_values = [entry['firstName'] + ' ' + entry['lastName'] for entry in filtered_data]
    x_values = [entry['total_leave_days'] for entry in filtered_data]

    return generate_bar_chart(x_values, y_values, 'Employee Leave Days', 'Total Leave Days', 'Employee')

def gen_leave_trend(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['year'] == filter_value]
    sorted_data = sorted(data, key=lambda entry: (entry['year'], entry['month']))
    x_labels = [f"{entry['year']}-{entry['month']}" for entry in sorted_data]
    y_values = [entry['leave_count'] for entry in sorted_data]

    return generate_line_chart(x_labels, y_values, 'Leave Trend', 'Year-Month', 'Leave Count')

def gen_leave_distribution(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['leavetypename'] == filter_value]
    leave_types = [entry['leavetypename'] for entry in data]
    leave_counts = [entry['leave_count'] for entry in data]

    return generate_pie_chart(leave_types, leave_counts, 'Leave Types Distribution')

def gen_leave_trend_fiscal_year(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['leavetypename'] == filter_value]
    start_dates = [datetime.strptime(entry['fiscal_start_date'], '%Y-%m-%dT%H:%M:%S%z').date() for entry in data]
    end_dates = [datetime.strptime(entry['fiscal_end_date'], '%Y-%m-%dT%H:%M:%S%z').date() for entry in data]
    leave_counts = [entry['leave_count'] for entry in data]
    leave_types = [entry['leavetypename'] for entry in data]
    unique_start_dates = sorted(list(set(start_dates)))
    unique_end_dates = sorted(list(set(end_dates)))
    unique_leave_types = sorted(list(set(leave_types)))
    data_traces = []
    for leave_type in unique_leave_types:
        leave_type_counts = [sum(leave_counts[i] for i in range(len(start_dates)) if leave_types[i] == leave_type and start_dates[i] == start and end_dates[i] == end) for start, end in zip(unique_start_dates, unique_end_dates)]
        bar = go.Bar(x=start_dates, y=leave_type_counts, name=leave_type)  # Assign leave_type directly to the name property
        data_traces.append(bar)

    layout = go.Layout(
        title='Leave Counts by Fiscal Year and Type',
        xaxis=dict(title='Fiscal Year'),
        yaxis=dict(title='Leave Count'),
        barmode='stack',
        margin=dict(l=40, r=10, t=50, b=40)
    )

    return go.Figure(data=data_traces, layout=layout)


def gen_department_leave_distribution(data, filter_value=None):
    department_leave_counts = {}
    leave_types = set()
    for entry in data:
        department = entry["departmentDescription"]
        leave_type = entry["leaveTypeName"]
        leave_count = entry["leave_count"]
        leave_types.add(leave_type)
        if department in department_leave_counts:
            department_leave_counts[department][leave_type] = leave_count
        else:
            department_leave_counts[department] = {leave_type: leave_count}
    departments = list(department_leave_counts.keys())
    if filter_value:
        leave_types = {filter_value}
    data_traces = []
    for leave_type in leave_types:
        leave_counts = [department_leave_counts[department].get(leave_type, 0) for department in departments]
        bar = go.Bar(name=leave_type, y=departments, x=leave_counts, orientation='h')
        data_traces.append(bar)

    layout = go.Layout(
        title='Leave Counts by Department and Type',
        xaxis=dict(title='Leave Count'),
        yaxis=dict(title='Department'),
        margin=dict(l=100, r=10, t=50, b=50)
    )

    return go.Figure(data=data_traces, layout=layout)

def gen_project_allocations(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['name'] == filter_value]
    sorted_data = sorted(data, key=lambda entry: entry['request_count'], reverse=True)
    top_data = sorted_data[:10]
    top_project_allocations = [entry['name'] for entry in top_data]
    top_project_allocations_counts = [entry['request_count'] for entry in top_data]

    title = 'Top 10 Project Allocations'
    x_title = 'Project Name'
    y_title = 'Request Count'

    trace = go.Bar(x=top_project_allocations, y=top_project_allocations_counts)
    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
        margin=dict(l=100, r=10, t=50, b=50)
    )

    return go.Figure(data=[trace], layout=layout)

