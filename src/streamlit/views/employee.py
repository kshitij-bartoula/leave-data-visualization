import streamlit as st
import plotly.express as px
import pandas as pd
from services.api_client import APIClient
from services.data_processor import DataProcessor
from datetime import datetime

class EmployeePage:
    def __init__(self):
        self.api = APIClient()
        self.processor = DataProcessor()

    def render(self):
        st.title("👥 Employee Overview")
        tab1, tab2 = st.tabs(["📋 Leave Details", "🧑‍💼 HR Details"])

        with tab1:
            self._render_leave_details()
        with tab2:
            self._render_hr_details()

    def _render_leave_details(self):
        st.subheader("🗓️ Employee Leave Information")
        df = self.api.fetch_data("employee_leave")
        if df is not None and not df.empty:

            date_cols = ['fiscalStartDate', 'fiscalEndDate', 'startDate', 'endDate']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y')
            
            col1, col2 = st.columns([3, 1])
            
            with col2:
                # Fiscal year filter
                if 'fiscalStartDate' in df.columns:
                    fiscal_options = ["All"] + sorted(df["fiscalStartDate"].unique())
                    fiscal_filter = st.selectbox(
                        "Filter by Fiscal Year",
                        options=fiscal_options,
                        key="leave_fiscal_filter"
                    )
                else:
                    fiscal_filter = "All"

            # Apply filters
            if fiscal_filter != "All":
                df = df[df["fiscalStartDate"] == fiscal_filter]

            # Display metrics if columns exist
            metric_cols = [col for col in ["total_leave_days"] if col in df.columns]
            if metric_cols:
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Total Employees", len(df))
                with metric_col2:
                    if 'total_leave_days' in df.columns:
                        avg_leave = df["total_leave_days"].mean()
                        st.metric("Average Leave Days", f"{avg_leave:.1f}")

            # Dynamic display columns
            possible_cols = [
                "empId", "firstName", "lastName",
                "fiscalId", "fiscalStartDate", "fiscalEndDate",
                "defaultDays", "transferableDays", "total_leave_days"
            ]
            display_cols = [col for col in possible_cols if col in df.columns]
            
            # Reset index and start from 1
            df_display = df[display_cols].reset_index(drop=True)
            df_display.index += 1

            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=False
            )
            # Visualization

            # Step 3: Get top 10 employees with highest leave days
            df_top10 = df.nlargest(10, 'total_leave_days')

            # Step 4: Choose appropriate x-axis column
            x_col = self._find_column(df_top10, ['firstName', 'empId', 'lastName'])

            # Step 5: Create bar chart
            fig = px.bar(
                df_top10,
                x=x_col,
                y=df_top10['total_leave_days'].round(0).astype(int).astype(str), 
                title=f"Top 10 Leave Days Distribution",
                labels={
                    'y': "Total Leave Days",
                    x_col: "Employee" if x_col == "firstName" else x_col
                },
                hover_data=[c for c in ["lastName", "defaultDays", "transferableDays", "total_leave_days"] if c in df.columns]
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No leave data available.")

    def _render_hr_details(self):
        st.subheader("🧾 Employee HR Details")
        df = self.api.fetch_data("hr_details")

        if df is not None and not df.empty:
            # Extract year from fiscal_start_date
            if "fiscal_start_date" in df.columns:
                df['fiscal_year'] = pd.to_datetime(df['fiscal_start_date'], errors='coerce').dt.year
            else:
                df['fiscal_year'] = None

            # Find common columns
            name_col = self._find_column(df, ['firstName', 'name', 'employeeName'])
            last_name_col = self._find_column(df, ['lastName', 'surname'])
            designation_col = self._find_column(df, ['designationName', 'designation', 'position'])

            col1, col2, col3 = st.columns([3, 2, 2])

            with col2:
                name_filter = st.text_input("🔍 Search by Name", key="hr_name_filter")

            with col3:
                # Designation filter
                if designation_col:
                    designation_options = ["All"] + sorted(df[designation_col].dropna().unique())
                    designation_filter = st.selectbox("Filter by Designation", options=designation_options, key="hr_designation_filter")
                else:
                    designation_filter = "All"

                # Fiscal Year filter
                if 'fiscal_year' in df.columns and df['fiscal_year'].notna().any():
                    fiscal_year_options = ["All"] + sorted(df['fiscal_year'].dropna().unique().astype(str), reverse=True)
                    fiscal_year_filter = st.selectbox("Filter by Fiscal Year", options=fiscal_year_options, key="hr_fiscal_year_filter")
                else:
                    fiscal_year_filter = "All"

            # Apply filters
            if name_filter and name_col:
                df = df[df[name_col].str.contains(name_filter, case=False, na=False)]
            if designation_filter != "All" and designation_col:
                df = df[df[designation_col] == designation_filter]
            if fiscal_year_filter != "All" and 'fiscal_year' in df.columns:
                df = df[df['fiscal_year'] == int(fiscal_year_filter)]

            # Prepare display columns
            possible_cols = ["empId", name_col, last_name_col, designation_col, "project_allocation", "fiscal_year"]
            display_cols = [col for col in possible_cols if col in df.columns and col is not None]

            # Reset index to start from 1
            df_display = df[display_cols].reset_index(drop=True)
            df_display.index += 1

            st.dataframe(df_display, use_container_width=True, hide_index=False)

            # Visualization
            if not df.empty and designation_col:
                st.markdown("#### 🧮 Employees by Designation")
                fig1 = px.pie(
                    df,
                    names=designation_col,
                    title="Designation Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No HR data available.")
    def _find_column(self, df, possible_names):
        """Helper to find a column with alternative names"""
        for name in possible_names:
            if name in df.columns:
                return name
        return None

def get_leave_distribution_chart(api: APIClient, fiscal_year: int = None):
    df = api.fetch_data("employee_leave")

    if df is not None and not df.empty and 'total_leave_days' in df.columns:
        # Filter by fiscal year if provided
        if fiscal_year and 'fiscalStartDate' in df.columns:
            df = df[df['fiscalStartDate'] == fiscal_year]

        # Identify x-axis column
        x_col = None
        for name in ['firstName', 'empId', 'lastName']:
            if name in df.columns:
                x_col = name
                break

        df_top10 = df.nlargest(10, 'total_leave_days')

        fig = px.bar(
            df_top10,
            x=x_col,
            y=df_top10['total_leave_days'].round(0).astype(int).astype(str),
            title=f"Top 10 Leave Days Distribution (Fiscal Year: {fiscal_year if fiscal_year else 'All'})",
            labels={
                x_col: "Employee" if x_col == "firstName" else x_col,
                "total_leave_days": "Total Leave Days"
            },
            hover_data=[
                c for c in [
                    "lastName", "defaultDays", "transferableDays", "total_leave_days", "fiscalStartDate", "fiscalEndDate"
                ] if c in df.columns
            ]
        )
        return fig

    return None

