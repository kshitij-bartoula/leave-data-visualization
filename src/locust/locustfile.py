from locust import HttpUser, task, between
import requests

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Time between consecutive requests

    @task
    def load_main_page(self):
        response = requests.get("http://plotly-dash:8050")
        assert response.status_code == 200

# from locust import HttpUser, task, between
# import dash
# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc
# from visualization.data_processing import (
#     employee_leave, leave_trend, leave_distribution,
#     leave_trend_fiscal_year, department_leave_distribution, leave_reason
# )
# from visualization.callbacks import register_callbacks


# from visualization import app
# class MyUser(HttpUser):
#     wait_time = between(1, 5)  # Time between consecutive requests

#     @task
#     def load_main_page(self):
#         self.client.get("/")
