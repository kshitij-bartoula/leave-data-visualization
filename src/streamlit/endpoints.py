# src/streamlit/endpoints.py
# from typing import Dict, Any

# # Configuration
# HOST = "fastapi" 

# # Full endpoint URLs
# ENDPOINTS = {
#     "employee_leave": f'http://{HOST}:8000/employee_leave_details',
#     "hr_details": f'http://{HOST}:8000/employee_HR_details',
#     "leave_balance": f'http://{HOST}:8000/leave_balance',
#     "leave_trend": f'http://{HOST}:8000/leave_trend',
#     "leave_distribution": f'http://{HOST}:8000/leave_distribution',
#     "fiscal_trend": f'http://{HOST}:8000/fiscal_year_leave_type_trend',
#     "dept_distribution": f'http://{HOST}:8000/department_leave_distribution',
#     "project_allocations": f'http://{HOST}:8000/top_10_project_allocations'
# }

# def get_endpoint(key: str) -> str:
#     """Get full endpoint URL by key"""
#     return ENDPOINTS.get(key, "")

# src/streamlit/endpoints.py
from typing import Dict, Any, Optional
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st

# Configuration
HOST = "fastapi"  # container name in Docker network

# Endpoint URLs
ENDPOINTS = {
    "employee_leave": f"http://{HOST}:8000/employee_leave_details",
    "hr_details": f"http://{HOST}:8000/employee_HR_details",
    "leave_trend": f"http://{HOST}:8000/leave_trend",
    "fiscal_trend": f"http://{HOST}:8000/fiscal_year_leave_type_trend",
    "dept_leave_distribution": f"http://{HOST}:8000/department_leave_distribution",
    "project_allocations": f"http://{HOST}:8000/top_10_project_allocations",
}


def get_endpoint(key: str) -> str:
    """Get full endpoint URL by key."""
    return ENDPOINTS.get(key, "")


def fetch_data(endpoint_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a FastAPI endpoint using HTTP Basic Auth credentials
    already stored in Streamlit session state.
    """
    url = get_endpoint(endpoint_key)
    username = st.session_state.get("username")
    password = st.session_state.get("password")  # ✅ must be stored during Streamlit login

    if not username or not password:
        st.error("Missing credentials to call FastAPI")
        return None

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data from {endpoint_key}: {e}")
        return None
