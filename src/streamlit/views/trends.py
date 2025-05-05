import streamlit as st
import plotly.express as px
from services.api_client import APIClient
from services.data_processor import DataProcessor

def get_monthly_trend_chart(api):
    df = api.fetch_data("leave_trend")
    if df is not None:
        fig = px.line(
                df,
                x="month",
                y=df['leave_count'].round(0).astype(int).astype(str),
                color="year",
                labels={
                    'month': 'Month',
                    'y': 'Leave Count'       
                },
                title="Monthly Leave Trends by Year"
        )
        return fig
    return None

def get_fiscal_trend_chart(api):
    df = api.fetch_data("fiscal_trend")
    if df is not None:
        fig = px.line(
                df,
                x="year",
                y=df['leave_count'].round(0).astype(int).astype(str),
                color="leavetypename",
                labels={
                    'year': 'Fiscal Year',
                    'y': 'Leave Count'  
                },
                title="Leave Trends by Fiscal Year and Leave Type",
                line_shape="linear",  
                markers=True  
        )
        return fig
    return None

class TrendsPage:
    def __init__(self):
        self.api = APIClient()
        self.processor = DataProcessor()

    def render(self):
        st.header("📈 Leave Trends")
        tab1, tab2 = st.tabs(["Monthly", "Fiscal Year"])

        with tab1:
            self._render_monthly_trends()
        with tab2:
            self._render_fiscal_trends()

    def _render_monthly_trends(self):
        st.subheader("Monthly Trends")
        df = self.api.fetch_data("leave_trend")
        if df is not None:
            year_filter = st.selectbox(
                "Filter by Year",
                options=["All"] + sorted(df["year"].unique()),
                key="trend_year"
            )
            filtered_df = self.processor.filter_data(df, "year", year_filter)
            fig = px.line(
                filtered_df,
                x="month",
                y=df['leave_count'].round(0).astype(int).astype(str),
                color="year",
                labels={
                    'month': 'Month',
                    'y': 'Leave Count',  
                    'year': 'Year'       
                },
                title="Monthly Leave Trends by Year"
            )
            st.plotly_chart(fig, use_container_width=True)

    def _render_fiscal_trends(self):
        st.subheader("Fiscal Year Trends")
        df = self.api.fetch_data("fiscal_trend")
        if df is not None:
            fig = px.line(
                df,
                x="fiscal_id",
                y=df['leave_count'].round(0).astype(int).astype(str),
                color="leavetypename",
                labels={
                    'fiscal_id': 'Fiscal Year',
                    'y': 'Leave Count',  
                    'leavetypename': 'Leave Type' 
                },
                title="Leave Trends by Fiscal Year and Leave Type",
                line_shape="linear",  
                markers=True  
            )
            st.plotly_chart(fig, use_container_width=True)
