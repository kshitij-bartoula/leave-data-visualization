from locust import HttpUser, task, between
from visualization.app import app

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Time between consecutive requests

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    @task
    def load_main_page(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

    @task
    def test_employee_dropdown(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the employee dropdown is rendered
            assert b'employee-dropdown' in response.data

    @task
    def test_leave_trend_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the leave trend graph is rendered
            assert b'leave-trend-graph' in response.data

    @task
    def test_leave_trend_fiscal_year_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the leave trend (fiscal year) graph is rendered
            assert b'leave-trend-fiscal-year-graph' in response.data

    @task
    def test_employee_leave_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the employee leave graph is rendered
            assert b'employee-leave-graph' in response.data

    @task
    def test_department_leave_distribution_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the department leave distribution graph is rendered
            assert b'department-leave-distribution-graph' in response.data

    @task
    def test_leave_reason_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the leave reason graph is rendered
            assert b'leave-reason-graph' in response.data

    @task
    def test_leave_distribution_graph(self):
        with self.app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            # Verify that the leave distribution graph is rendered
            assert b'leave-distribution-graph' in response.data


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
