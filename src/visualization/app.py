# visualization/app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Leave Visualization Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='filter-dropdown',
                options=[
                    {'label': 'Employee Leave Days', 'value': 'employee_leave'},
                    {'label': 'Leave Balance', 'value': 'leave_balance'},
                    {'label': 'Leave Trend', 'value': 'leave_trend'},
                    {'label': 'Leave Types Distribution', 'value': 'leave_distribution'},
                    {'label': 'Leave Counts by Fiscal Year and Type', 'value': 'leave_trend_fiscal_year'},
                    {'label': 'Leave Counts by Department and Type', 'value': 'department_leave_distribution'},
                    {'label': 'Top 5 Leave Reasons', 'value': 'leave_reason'}
                ],
                value='employee_leave',
                className='mb-4'
            ),
            dcc.Dropdown(
                id='filter-value-dropdown',
                className='mb-4'
            ),
            dcc.Graph(id='data-chart', className='graph-container')
        ])
    ]),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
], fluid=True, className='content', style={'backgroundColor': '#f0f2f5'})

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
