import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'])

# Read environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
database_url = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
api_endpoint = os.getenv('API_ENDPOINT')
bearer_token = os.getenv('BEARER_TOKEN')

# Function to generate a card with a graph
def generate_graph_card(graph_id, graph_title):
    return dbc.Card(
        dbc.CardBody([
            html.H4(graph_title, className="card-title"),
            dcc.Graph(id=graph_id, className="graph-container")
        ]),
        className="mb-3"
    )

def generate_employee_dropdown():
    employee_dropdown = dcc.Dropdown(
        id='employee-dropdown',
        options=[],  # Options will be populated dynamically
        placeholder='Select an employee...',
        multi=False  # Set to True if you want to allow selecting multiple employees
    )
    return employee_dropdown

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Leave Visualization Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),
    # dbc.Row([
    #     dbc.Col(generate_graph_card('employee-leave-graph', 'Employee Leave Days'), width=12),
    # ]),
    dbc.Row([
        dbc.Col(generate_graph_card('leave-trend-graph', 'Leave Trend'), width=12),
        dbc.Col(generate_graph_card('leave-trend-fiscal-year-graph', 'Leave Trend (Fiscal Year)'), width=12),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Employee Leave Days"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='employee-dropdown',
                                            options=[],  # Options will be populated dynamically
                                            placeholder='Select an employee...',
                                            multi=False  # Set to True if you want to allow selecting multiple employees
                                        ),
                                        width=3
                                    )  # Adjust width as needed
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(id='employee-leave-graph', className='graph-container'))  # Employee Leave Days
                                ]
                            )
                        ]
                    )
                ]
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(generate_graph_card('department-leave-distribution-graph', 'Department Leave Distribution'), width=12),
    ]),
    dbc.Row([
        dbc.Col(generate_graph_card('leave-reason-graph', 'Leave Reasons'), width=6),
        dbc.Col(generate_graph_card('leave-distribution-graph', 'Leave Distribution'), width=6),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
], fluid=True, className='content', style={'backgroundColor': '#5fb9d7'})

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
