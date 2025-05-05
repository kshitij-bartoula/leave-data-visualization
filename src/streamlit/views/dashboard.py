import streamlit as st
from datetime import datetime
import plotly.express as px
import pandas as pd

class DashboardPage:
    def render_sidebar(self):
        st.markdown("---")
        st.markdown(f"**Last Refresh:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("🔄 Reload Data", key="reload_data_button"):
            st.cache_data.clear()

    def render_header(self):
        st.title("📊 Leave Analytics Dashboard")

    def render_home(self):
        # Visually enhanced welcome section
        st.markdown("""
            <div style="padding: 2rem; border-radius: 15px; background: linear-gradient(to right, #f0f2f6, #ffffff); text-align: center;">
                <h1 style="color: #3b5998;">👋 Welcome to the Leave Analytics Portal</h1>
                <p style="font-size: 1.2rem; color: #333;">
                    Analyze employee leave trends, department summaries, and organizational behavior patterns at a glance.
                </p>
                <p style="font-size: 1rem; color: #555;">
                    Use the navigation panel to explore dashboards tailored to different aspects of your data.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            ### 🚀 key Features:
            - 📊 Trend analysis of leaves by month  
            - 🧑‍💼 Employee-level leave tracking  
            - 🏢 Department-wise analytics  
            - ⏱️ Real-time data reload capability  
        """)
