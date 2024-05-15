import requests

def employee_leave(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle API request error
        return []

def leave_balance(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle API request error
        return []

def leave_trend(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return('error feching leave trend data from api')

def leave_distribution(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def leave_trend_fiscal_year(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def department_leave_distribution(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def leave_reason(endpoint_url):
    api_url = endpoint_url
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []






