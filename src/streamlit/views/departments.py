import streamlit as st
import plotly.express as px
import pandas as pd
from services.api_client import APIClient
from services.data_processor import DataProcessor

def get_department_distribution_chart(api):
    df = api.fetch_data("dept_leave_distribution")
    if df is not None:
        df["fiscal_year"] = df["fiscal_start_date"] + " to " + df["fiscal_end_date"]

        fig = px.bar(
            df,
            x="departmentDescription",
            y=df['leave_count'].round(0).astype(int).astype(str),
            barmode="group",
            labels={
                "departmentDescription": "Department",
                'y': "Leave Count"
            },
            title="Leave Distribution by Department and Type"
        )
        return fig
    return None

def get_department_allocation_count_chart(api):
    df = api.fetch_data("project_allocations")
    if df is not None:
        fig = px.bar(
            df, 
            x="name", 
            y=df['request_count'].round(0).astype(int).astype(str),
            labels={
                'y': 'Number of Employee',  # Renames y-axis
                'name': 'Project Name'     # Renames x-axis
            }
        )
        return fig
    return None

class DepartmentsPage:
    def __init__(self):
        self.api = APIClient()
        self.processor = DataProcessor()

    def render(self):
        st.header("🏢 Department Overview")
        tab1, tab2 = st.tabs(["Department leave status", "Allocations"])

        with tab1:
            self._render_status()
        with tab2:
            self._render_allocations()

    def _render_status(self):
        st.subheader("Leave Status by Department")
        df = self.api.fetch_data("dept_leave_distribution")
        if df is not None:
            # Convert to datetime and extract year
            df["fiscal_start_date"] = pd.to_datetime(df["fiscal_start_date"])
            df["fiscal_year"] = df["fiscal_start_date"].dt.year

            # Fiscal year filter
            fiscal_year_filter = st.selectbox(
                "Filter by Fiscal Year",
                options=["All"] + sorted(df["fiscal_year"].unique(), reverse=True),
                key="fiscal_year_filter"
            )

            if fiscal_year_filter != "All":
                df = df[df["fiscal_year"] == fiscal_year_filter]

            # Department filter
            dept_filter = st.selectbox(
                "Filter by Department",
                options=["All"] + sorted(df["departmentDescription"].unique()),
                key="dept_status"
            )

            filtered_df = self.processor.filter_data(df, "departmentDescription", dept_filter)

            # Chart
            fig = px.bar(
                filtered_df,
                x="departmentDescription",
                y="leave_count",
                color="leaveTypeName",
                barmode="group",
                labels={
                    "departmentDescription": "Department",
                    "leaveTypeName": "Leave Type",
                    "leave_count": "Leave Count"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    def _render_allocations(self):
        st.subheader("Project Allocations")
        df = self.api.fetch_data("project_allocations")
        if df is not None:
            fig = px.bar(
                df, 
                x="name", 
                y=df['request_count'].round(0).astype(int).astype(str),
                labels={
                    'y': 'Number of Employee',  
                    'name': 'Project Name'     
                }
            )
            st.plotly_chart(fig, use_container_width=True)
