import streamlit as st
from services.api_client import APIClient
from services.data_processor import DataProcessor

# Import reusable chart functions
from views.employee import (
    get_leave_distribution_chart
)
from views.trends import (
    get_monthly_trend_chart,
    get_fiscal_trend_chart
)
from views.departments import (
    get_department_distribution_chart,
    get_department_allocation_count_chart
)

class OverviewPage:
    def __init__(self):
        self.api = APIClient()
        self.processor = DataProcessor()

    def render(self):
        st.title("📊 Overview Dashboard")

        # Employee Leave Section
        st.markdown("### 🧍 Employee Leave") 
        col1 = st.columns(1)[0]  
        with col1:
            st.subheader("Leave Distribution")
            fig1 = get_leave_distribution_chart(self.api)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No leave distribution data available.")

        # Leave Trends Section
        st.markdown("### 📈 Leave Trends")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Monthly Trends")
            fig3 = get_monthly_trend_chart(self.api)
            if fig3:
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No monthly trend data available.")
        
        with col4:
            st.subheader("Fiscal Year Trends")
            fig4 = get_fiscal_trend_chart(self.api)
            if fig4:
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No fiscal trend data available.")

        # Department Section
        st.markdown("### 🏢 Department Overview")
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("Department Distribution")
            fig5 = get_department_distribution_chart(self.api)
            if fig5:
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("No department distribution data available.")

        with col6:
            st.subheader("Department Allocation Summary")
            fig6 = get_department_allocation_count_chart(self.api)
            if fig6:
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("No department leave summary data available.")
