import streamlit as st
import plotly.express as px
from services.api_client import APIClient
from services.data_processor import DataProcessor

class LeaveAnalyticsPage:
    def __init__(self):
        self.api = APIClient()
        self.processor = DataProcessor()
    
    def render(self):
        st.header("🧾 Leave Analytics")
        tab1, tab2 = st.tabs(["Balances", "Distribution"])
        
        with tab1:
            self._render_balances()
        with tab2:
            self._render_distribution()
    
    def _render_balances(self):
        st.subheader("Leave Balances")
        df = self.api.fetch_data("leave_balance")
        if df is not None:
            col1, col2 = st.columns([3, 1])
            with col2:
                dept_filter = st.selectbox(
                    "Filter by Department", 
                    options=["All"] + sorted(df["departmentDescription"].unique()),
                    key="balance_dept"
                )
            filtered_df = self.processor.filter_data(df, "departmentDescription", dept_filter)
            st.dataframe(filtered_df, use_container_width=True)
    
    def _render_distribution(self):
        st.subheader("Leave Type Distribution")
        df = self.api.fetch_data("leave_distribution")
        if df is not None:
            fig = px.pie(df, values="leave_count", names="leavetypename")
            st.plotly_chart(fig, use_container_width=True)
