import requests
import json
import pandas as pd
from sqlalchemy import create_engine
from utils.db_utils import connection
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv

# Function to ingest data from API
def ingest_api_data(API_ENDPOINT, headers):
    all_data = []
    page = 1
    while True:
        params = {'page': page}
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            all_data.extend(data['data'])  # Assuming the response contains a 'data' key with the actual data
            if not data.get('next_page'):
                break  # Exit the loop if there's no next page
            page += 1
        else:
            print(f"Failed to fetch data from page {page}. Status code: {response.status_code}")
            break  # Exit the loop if there's an error fetching data
    return all_data

# Function to insert data into PostgreSQL database
def insert_data_to_db(data, db_engine, table_name, schema='public'):
    try:
        data.to_sql(table_name, db_engine, schema=schema, if_exists='replace', index=False)
        print(f"Data inserted into PostgreSQL table '{schema}.{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting data into PostgreSQL table '{schema}.{table_name}':", str(e))

# Function to parse JSON data and separate nested JSON into a different table
def parse_json_and_insert(api_data, db_engine):
    main_data = []
    nested_data = []
    for entry in api_data:
        main_entry = entry.copy()  # Create a copy of the entry for the main table
        allocations = main_entry.pop('allocations', None)  # Remove allocations from the main entry
        if allocations is not None and isinstance(allocations, list):
            main_entry['allocations'] = json.dumps(allocations)  # Add allocations in JSON format to main entry
            for alloc_item in allocations:
                nested_entry = {'empId': main_entry['empId']}  # Include parent_id for relationship
                nested_entry.update(alloc_item)  # Add allocation data to nested entry
                nested_data.append(nested_entry)  # Append nested entry to list
        main_data.append(main_entry)  # Append main entry to list
    df_main = pd.DataFrame(main_data)  # Create DataFrame for main data
    df_nested = pd.DataFrame(nested_data)  # Create DataFrame for nested data

    # Insert main data into PostgreSQL table
    insert_data_to_db(df_main, db_engine, 'api_data', schema='raw')

    # Insert nested data into PostgreSQL table
    insert_data_to_db(df_nested, db_engine, 'allocation_data', schema='raw')


load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_ENDPOINT = os.getenv('API_ENDPOINT')

headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

# Access configuration settings
db_engine = connection()

with db_engine.connect() as conn:
    schema_existence_query = text("SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'raw')")
    schema_exists = conn.execute(schema_existence_query).scalar()

    if not schema_exists:
        print('Schema not exists. creating schema...')
        create_schema_query = text("CREATE SCHEMA raw")
        conn.execute(create_schema_query)
    else:
        print('raw_schema exists')

# Ingest data from API
api_data = ingest_api_data(API_ENDPOINT, headers)

# Parse JSON data and insert into PostgreSQL tables
if api_data:
    print(api_data)
    parse_json_and_insert(api_data, db_engine)
else:
    print("No data fetched from API.")
