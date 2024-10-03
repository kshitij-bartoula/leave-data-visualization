import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'])

# Function to generate a card with a graph
def generate_graph_card(graph_id, graph_title):
    return dbc.Card(
        dbc.CardBody([
            html.H4(graph_title, className="card-title"),
            dcc.Graph(id=graph_id, className="graph-container")
        ]),
        className="mb-3"
    )

def generate_employee_dropdown(id):
    employee_dropdown = dcc.Dropdown(
        id=id,
        options=[],  # Options will be populated dynamically
        placeholder='Select an employee...',
        multi=False  # Set to True if you want to allow selecting multiple employees
    )
    return employee_dropdown

def generate_project_dropdown():
    project_dropdown = dcc.Dropdown(
        id='project-dropdown',
        options=[],  # Options will be populated dynamically
        placeholder='Select project...',
        multi=False  # Set to True if you want to allow selecting multiple projects
    )
    return project_dropdown

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Leave Visualization Dashboard", className="text-center text-primary mb-4"), width=24)
    ]),
    # dbc.Row([
    #     dbc.Col(generate_graph_card('employee-leave-graph', 'Employee Leave Days'), width=12),
    # ]),
    dbc.Row([
        dbc.Col(generate_graph_card('leave-trend-graph', 'Leave Trend'), width=6),
        dbc.Col(generate_graph_card('leave-trend-fiscal-year-graph', 'Leave Count (Fiscal Year)'), width=6),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Employee Leave Days"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(generate_employee_dropdown('employee-leave-dropdown'), width=4)  # Employee dropdown
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='employee-leave-graph', className='graph-container'))  # Employee Leave Days graph
                    ])
                ])
            ]),
            width=12
        )
    ]),
    # New Row for Employee Details Table and Dropdown
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Employee Details", className="card-header"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(generate_employee_dropdown('employee-details-dropdown'), width=4),  # Employee dropdown
                        dbc.Col(generate_project_dropdown(), width=4)
                    ]),
                    dbc.Row([
                        DataTable(
                            id='employee-details-table',
                            columns=[
                                {'name': 'Employee ID', 'id': 'empId'},
                                {'name': 'First Name', 'id': 'firstName'},
                                {'name': 'Last Name', 'id': 'lastName'},
                                {'name': 'Fiscal Start Date', 'id': 'fiscal_start_date'},
                                {'name': 'Fiscal End Date', 'id': 'fiscal_end_date'},
                                {'name': 'Designation', 'id': 'designationName'},
                                {'name': 'Project Allocation', 'id': 'project_allocation'},
                            ],
                            data=[],  # This will be filled by the callback
                            style_table={'overflowX': 'auto'},
                            page_size=10,  # Number of rows per page
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'border': '1px solid #ddd',
                                'backgroundColor': '#ffffff'  # White background for the table
                            },
                            style_header={
                                'backgroundColor': '#c15226',  # Light grey for header
                                'fontWeight': 'bold'
                            }
                        )
                    ])
                ])
            ], className="card-employee-details"),  # Apply specific card color class
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(generate_graph_card('department-leave-distribution-graph', 'Department Leave Distribution'), width=12),
    ]),
    dbc.Row([
        dbc.Col(generate_graph_card('project-allocations-graph', 'Project Allocations'), width=6),
        dbc.Col(generate_graph_card('leave-distribution-graph', 'Leave Distribution'), width=6),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
], fluid=True, className='content', style={'backgroundColor': '#5fb9d7'})


if __name__ == "__main__":
    register_callbacks(app)
    app.run_server(debug=True, host='0.0.0.0')
