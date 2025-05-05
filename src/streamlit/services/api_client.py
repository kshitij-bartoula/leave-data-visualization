# import requests
# import pandas as pd
# from typing import Optional
# from endpoints import get_endpoint

# class APIClient:
#     @staticmethod
#     def fetch_data(endpoint_key: str) -> Optional[pd.DataFrame]:
#         """Generic data fetcher for all endpoints"""
#         url = get_endpoint(endpoint_key)

#         # 🛡️ Check if URL exists
#         if not url:
#             print(f"[Warning] No URL found for endpoint key: '{endpoint_key}'")
#             return None

#         try:
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
#             return pd.DataFrame(response.json())
#         except Exception as e:
#             print(f"[Error] API Error while fetching '{endpoint_key}': {str(e)}")
#             return None

# api_client.py

import requests
import pandas as pd
import streamlit as st
from typing import Optional
from endpoints import get_endpoint
from requests.auth import HTTPBasicAuth


class APIClient:
    @staticmethod
    def fetch_data(endpoint_key: str) -> Optional[pd.DataFrame]:
        """Generic data fetcher with Streamlit session-based auth."""
        url = get_endpoint(endpoint_key)

        if not url:
            print(f"[Warning] No URL found for endpoint key: '{endpoint_key}'")
            return None

        # Inject credentials from session
        username = st.session_state.get("username")
        password = st.session_state.get("password")
        if not username or not password:
            print(f"[Error] Missing credentials in session for {endpoint_key}")
            return None

        try:
            response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=10)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except Exception as e:
            print(f"[Error] API Error while fetching '{endpoint_key}': {str(e)}")
            return None
