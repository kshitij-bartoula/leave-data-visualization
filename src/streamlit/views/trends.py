import streamlit as st
import calendar
import plotly.express as px
import pandas as pd
from services.api_client import APIClient
from services.data_processor import DataProcessor

def get_monthly_trend_chart(api):
    df = api.fetch_data("leave_trend")
    if df is not None:
        # Convert month number to abbreviated month name
        df['month_name'] = df['month'].apply(lambda x: calendar.month_abbr[int(x)])
        
        # Optional: sort by month number to maintain correct order in x-axis
        df['month_order'] = df['month']
        df = df.sort_values(by='month_order')

        fig = px.line(
            df,
            x="month_name",
            y=df['leave_count'].round(0).astype(int).astype(str),
            color="year",
            labels={
                'month_name': 'Month',
                'y': 'Leave Count'
            },
            title="Monthly Leave Trends by Year"
        )
        return fig

    return None

def get_fiscal_trend_chart(api):
    df = api.fetch_data("fiscal_trend")

    if df is not None and not df.empty:
        # Extract and convert fiscal year to string
        df['year'] = pd.to_datetime(df['fiscal_start_date'], errors='coerce').dt.year.astype(str)

        # Drop rows with missing years
        df = df.dropna(subset=['year'])

        # Sort years if needed
        df = df.sort_values('year')

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

        # Force x-axis to be categorical (no intermediate values)
        fig.update_layout(xaxis_type='category')

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
        fig = get_monthly_trend_chart(self.api)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for monthly trends.")

    def _render_fiscal_trends(self):
        st.subheader("Fiscal Year Trends")
        fig = get_fiscal_trend_chart(self.api)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for fiscal trends.")

