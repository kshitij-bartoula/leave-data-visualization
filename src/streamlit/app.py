# import streamlit as st
# from auth.database import get_db
# from auth.auth import verify_login
# from views.dashboard import DashboardPage
# from views.overview import OverviewPage
# from views.employee import EmployeePage
# from views.trends import TrendsPage
# from views.departments import DepartmentsPage


# def main():
#     st.set_page_config(page_title="Leave Analytics", layout="wide")

#     # Initialize session state for login
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False
#     if "username" not in st.session_state:
#         st.session_state.username = ""

#     # Show login form if not authenticated
#     if not st.session_state.logged_in:
#         st.title("🔐 Login to Leave Analytics Dashboard")
#         with st.form("login_form", clear_on_submit=False):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             submitted = st.form_submit_button("Login")

#         if submitted:
#             db = next(get_db())
#             if verify_login(username, password, db):
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.success("✅ Login successful!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid username or password")
#         return  # Stop rendering the dashboard

#     # ================= Render Dashboard ===============
#     dashboard = DashboardPage()
#     dashboard.render_header()

#     # Sidebar navigation and logout
#     with st.sidebar:
#         st.markdown(f"👋 Welcome, **{st.session_state.username}**")
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.rerun()

#         dashboard.render_sidebar()
#         selected_tab = st.radio(
#             "Navigation",
#             ["🏠 Home", "📊 Overview", "👥 Employees", "📈 Trends", "🏢 Departments"],
#             key="main_nav"
#         )

#     # Tab routing
#     if selected_tab == "🏠 Home":
#         dashboard.render_home()
#     elif selected_tab == "📊 Overview":
#         OverviewPage().render()
#     elif selected_tab == "👥 Employees":
#         EmployeePage().render()
#     elif selected_tab == "📈 Trends":
#         TrendsPage().render()
#     elif selected_tab == "🏢 Departments":
#         DepartmentsPage().render()


# if __name__ == "__main__":
#     main()

# app.py

import streamlit as st
from auth.database import get_db
from auth.auth import verify_login
from views.dashboard import DashboardPage
from views.overview import OverviewPage
from views.employee import EmployeePage
from views.trends import TrendsPage
from views.departments import DepartmentsPage
from services.api_client import APIClient  # Required to fetch from FastAPI with auth


def login_screen():
    """Handles the login screen and authentication."""
    st.title("🔐 Login to Leave Analytics Dashboard")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        db = next(get_db())
        if verify_login(username, password, db):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.password = password  # Store for API auth
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")


def logout():
    """Clears the session state and logs the user out."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.password = ""


def render_dashboard():
    """Renders the main dashboard and handles navigation."""
    dashboard = DashboardPage()
    dashboard.render_header()

    with st.sidebar:
        st.markdown(f"👋 Welcome, **{st.session_state.username}**")
        if st.button("Logout"):
            logout()
            st.rerun()

        dashboard.render_sidebar()
        selected_tab = st.radio(
            "Navigation",
            ["🏠 Home", "📊 Overview", "👥 Employees", "📈 Trends", "🏢 Departments"],
            key="main_nav"
        )

    if selected_tab == "🏠 Home":
        dashboard.render_home()
    elif selected_tab == "📊 Overview":
        OverviewPage().render()
    elif selected_tab == "👥 Employees":
        EmployeePage().render()
    elif selected_tab == "📈 Trends":
        TrendsPage().render()
    elif selected_tab == "🏢 Departments":
        DepartmentsPage().render()


def main():
    st.set_page_config(page_title="Leave Analytics", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "password" not in st.session_state:
        st.session_state.password = ""

    if not st.session_state.logged_in:
        login_screen()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
