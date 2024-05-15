# visualization/components.py
import plotly.graph_objs as go
from datetime import datetime

def gen_employee_leave(data, filter_value=None, default_count=10):
    if filter_value:
        data = [entry for entry in data if filter_value in (entry['firstName'] + ' ' + entry['lastName'])]
    else:
        data = data[:default_count]  # Show only the first `default_count` employees by default

    x_values = [entry['firstName'] + ' ' + entry['lastName'] for entry in data]
    y_values = [entry['total_leave_days'] for entry in data]

    trace = go.Bar(y=x_values, x=y_values, orientation='h')
    layout = go.Layout(
        title='Employee Leave Days',
        xaxis=dict(title='Total Leave Days'),
        yaxis=dict(title='Employee'),
        margin=dict(l=100, r=10, t=50, b=50)
    )
    figure = go.Figure(data=[trace], layout=layout)
    return figure

def gen_employee_leave_filter_options(data):
    employee_names = [entry['firstName'] + ' ' + entry['lastName'] for entry in data]
    return [{'label': name, 'value': name} for name in sorted(set(employee_names))]

def gen_leave_balance(data, filter_value=None, default_count=10):
    if filter_value:
        data = [entry for entry in data if filter_value in (entry['firstName'] + ' ' + entry['lastName'])]
    else:
        data = data[:default_count]
        
    x_values = [entry['firstName'] + ' ' + entry['lastName'] for entry in data]
    y_values = [entry['leave_balance'] for entry in data]
    trace = go.Bar(x=x_values, y=y_values)
    layout = go.Layout(
        title='Leave Balance',
        xaxis=dict(title='Employee'),
        yaxis=dict(title='Leave Balance'),
        margin=dict(l=40, r=10, t=50, b=100)
    )
    figure = go.Figure(data=[trace], layout=layout)
    return figure

def gen_leave_balance_filter_options(data):
    employee_names = [entry['firstName'] + ' ' + entry['lastName'] for entry in data]
    return [{'label': name, 'value': name} for name in sorted(set(employee_names))]

def gen_leave_trend(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['year'] == filter_value]
    sorted_data = sorted(data, key=lambda entry: (entry['year'], entry['month']))
    x_labels = [f"{entry['year']}-{entry['month']}" for entry in sorted_data]
    y_values = [entry['leave_count'] for entry in sorted_data]
    trace = go.Scatter(x=x_labels, y=y_values, mode='lines+markers')
    layout = go.Layout(
        title='Leave Trend',
        xaxis=dict(title='Year-Month'),
        yaxis=dict(title='Leave Count'),
        margin=dict(l=40, r=10, t=50, b=40)
    )
    figure = go.Figure(data=[trace], layout=layout)
    return figure

def gen_leave_trend_filter_options(data):
    years = [entry['year'] for entry in data]
    return [{'label': str(year), 'value': year} for year in sorted(set(years))]

def gen_leave_distribution(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['leavetypename'] == filter_value]
    leave_types = [entry['leavetypename'] for entry in data]
    leave_counts = [entry['leave_count'] for entry in data]
    trace = go.Pie(labels=leave_types, values=leave_counts)
    layout = go.Layout(
        title='Leave Types Distribution',
        margin=dict(l=40, r=10, t=50, b=40)
    )
    figure = go.Figure(data=[trace], layout=layout)
    return figure

def gen_leave_distribution_filter_options(data):
    leave_types = [entry['leavetypename'] for entry in data]
    return [{'label': leavetype, 'value': leavetype} for leavetype in sorted(set(leave_types))]

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
    fiscal_years = [f"{start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}" for start, end in zip(unique_start_dates, unique_end_dates)]
    data_traces = []
    for leave_type in unique_leave_types:
        leave_type_counts = [sum(leave_counts[i] for i in range(len(start_dates)) if leave_types[i] == leave_type and start_dates[i] == start and end_dates[i] == end) for start, end in zip(unique_start_dates, unique_end_dates)]
        bar = go.Bar(name=leave_type, x=fiscal_years, y=leave_type_counts)
        data_traces.append(bar)
    layout = go.Layout(
        title='Leave Counts by Fiscal Year and Type',
        xaxis=dict(title='Fiscal Year'),
        yaxis=dict(title='Leave Count'),
        barmode='stack',
        margin=dict(l=40, r=10, t=50, b=40)
    )
    figure = go.Figure(data=data_traces, layout=layout)
    return figure

def gen_leave_trend_fiscal_year_filter_options(data):
    leave_types = [entry['leavetypename'] for entry in data]
    return [{'label': leavetype, 'value': leavetype} for leavetype in sorted(set(leave_types))]

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
    figure = go.Figure(data=data_traces, layout=layout)
    return figure

def gen_department_leave_distribution_filter_options(data):
    leave_types = [entry['leaveTypeName'] for entry in data]
    return [{'label': leavetype, 'value': leavetype} for leavetype in sorted(set(leave_types))]

def gen_leave_reason(data, filter_value=None):
    if filter_value:
        data = [entry for entry in data if entry['reason'] == filter_value]
    sorted_data = sorted(data, key=lambda entry: entry['request_count'], reverse=True)
    top_data = sorted_data[:5]
    top_leave_reasons = [entry['reason'] for entry in top_data]
    top_leave_request_counts = [entry['request_count'] for entry in top_data]
    trace = go.Pie(labels=top_leave_reasons, values=top_leave_request_counts)
    layout = go.Layout(
        title='Top 5 Leave Reasons',
        margin=dict(l=40, r=10, t=50, b=40)
    )
    figure = go.Figure(data=[trace], layout=layout)
    return figure

def gen_leave_reason_filter_options(data):
    reasons = [entry['reason'] for entry in data]
    return [{'label': reason, 'value': reason} for reason in sorted(set(reasons))]
