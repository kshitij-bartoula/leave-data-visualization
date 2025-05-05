
import os
import json
import logging
import requests
import pandas as pd
from sqlalchemy.sql import text
from utils.db_utils import connection

logger = logging.getLogger(__name__)

# Function to ingest data from API
def ingest_api_data(API_ENDPOINT, headers):
    all_data = []
    page = 1
    while True:
        params = {'page': page}
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['data'])  # Assuming the response contains a 'data' key with the actual data
            if not data.get('next_page'):
                break  # Exit the loop if there's no next page
            page += 1
        else:
            logger.error(f"Failed to fetch data from page {page}. Status code: {response.status_code}")
            break  # Exit the loop if there's an error fetching data
    return all_data

# Function to insert data into PostgreSQL database
def insert_data_to_db(data, db_engine, table_name, schema):
    try:
        data.to_sql(table_name, db_engine, schema=schema, if_exists='replace', index=False)
        logger.info(f"Data inserted into PostgreSQL table '{schema}.{table_name}' successfully.")
    except Exception as e:
        logger.error(f"Error inserting data into PostgreSQL table '{schema}.{table_name}': {str(e)}")

# Function to parse JSON data and separate nested JSON into a different table
def parse_json_and_insert(api_data, db_engine):
    main_data = []
    nested_data = []
    for entry in api_data:
        main_entry = entry.copy()
        allocations = main_entry.pop('allocations', None)
        if allocations is not None and isinstance(allocations, list):
            main_entry['allocations'] = json.dumps(allocations)
            for alloc_item in allocations:
                nested_entry = {'empId': main_entry['empId']}
                nested_entry.update(alloc_item)
                nested_data.append(nested_entry)
        main_data.append(main_entry)
    df_main = pd.DataFrame(main_data)
    df_nested = pd.DataFrame(nested_data)

    # Insert main data into PostgreSQL table
    insert_data_to_db(df_main, db_engine, 'api_data', schema='raw')

    # Insert nested data into PostgreSQL table
    insert_data_to_db(df_nested, db_engine, 'allocation_data', schema='raw')


def main():

    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    API_ENDPOINT = os.getenv('API_ENDPOINT')

    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }

    db_engine = connection()

    # Ingest data from API
    api_data = ingest_api_data(API_ENDPOINT, headers)

    # Parse JSON data and insert into PostgreSQL tables
    if api_data:
        parse_json_and_insert(api_data, db_engine)
    else:
        logger.warning("No data fetched from API.")

if __name__ == "__main__":
    main()
