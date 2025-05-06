import os, json, requests, pandas as pd
from sqlalchemy.sql import text
from utils.db_utils import connection
import logging

logger = logging.getLogger(__name__)

def ingest_api_data(API_ENDPOINT, headers):
    all_data, page = [], 1
    while True:
        try:
            response = requests.get(API_ENDPOINT, headers=headers, params={'page': page})
            if response.status_code == 200:
                data = response.json()
                all_data.extend(data.get('data', []))
                if not data.get('next_page'):
                    break
                page += 1
            else:
                raise ValueError(f"Failed on page {page}, status {response.status_code}")
        except Exception as e:
            logger.error("API ingestion failed", exc_info=True)
            raise
    return all_data

def insert_data_to_db(dataframe, db_engine, table_name, schema):
    try:
        dataframe.to_sql(table_name, db_engine, schema=schema, if_exists='replace', index=False)
    except Exception as e:
        logger.error(f"Inserting to {schema}.{table_name} failed", exc_info=True)
        raise

def parse_json_and_insert(api_data, db_engine):
    try:
        main_data, nested_data = [], []

        for entry in api_data:
            main_entry = entry.copy()
            allocations = main_entry.pop('allocations', None)
            if allocations:
                main_entry['allocations'] = json.dumps(allocations)
                for alloc in allocations:
                    nested_data.append({'empId': main_entry['empId'], **alloc})
            main_data.append(main_entry)

        df_main = pd.DataFrame(main_data)
        df_nested = pd.DataFrame(nested_data)

        insert_data_to_db(df_main, db_engine, 'api_data', 'raw')
        insert_data_to_db(df_nested, db_engine, 'allocation_data', 'raw')

    except Exception as e:
        logger.error("Parsing or DB insertion failed", exc_info=True)
        raise

def main():
    try:
        BEARER_TOKEN = os.getenv('BEARER_TOKEN')
        API_ENDPOINT = os.getenv('API_ENDPOINT')
        if not BEARER_TOKEN or not API_ENDPOINT:
            raise EnvironmentError("Missing BEARER_TOKEN or API_ENDPOINT")

        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        db_engine = connection()
        api_data = ingest_api_data(API_ENDPOINT, headers)

        if api_data:
            parse_json_and_insert(api_data, db_engine)
    except Exception as e:
        logger.error("API ingestion main() failed", exc_info=True)
        raise
