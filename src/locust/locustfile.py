# from locust import HttpUser, between, task

# class PlotlyDashUser(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def load_main_page(self):
#         self.client.get("/")

#     @task
#     def load_graphs(self):
#         self.client.get("/graphs")
#         self.client.get("/graphs/employee-leave")
#         self.client.get("/graphs/leave-trend")
#         self.client.get("/graphs/leave-distribution")


from locust import HttpUser, task, between


# Import the plotly Dash app
from src.visualization import app


class MyUser(HttpUser):
    wait_time = between(1, 5)  # Time between consecutive requests

    @task
    def load_main_page(self):
        self.client.get("/")
