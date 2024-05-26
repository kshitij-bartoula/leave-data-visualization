from utils.config_utils import get_db_config
from sqlalchemy import create_engine
from pathlib import Path
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.dialects import postgresql

def connection():
    db_config = get_db_config()
    DB_USERNAME = db_config['DB_USERNAME']
    DB_PASSWORD = db_config['DB_PASSWORD']
    DB_HOST = db_config['DB_HOST']
    DB_NAME = db_config['DB_NAME']

    if all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
        DB_CONNECTION_STR = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
        db_engine = create_engine(DB_CONNECTION_STR)
        return db_engine
    else:
        raise ValueError("One or more database connection variables are missing in environment variables.")

def execute_sql_from_file(sql_file_path, db_engine):
    try:
        with db_engine.connect() as con:
            with open(sql_file_path, 'r') as sql_file:
                query = text(sql_file.read())
                con.execute(query)
        print(f"query executed successfully for sql from file")
    except Exception as e:
        print(f"Error executing SQL queries from file: {e}")


def get_result_from_query(query_statement):
    db_engine = connection()
    print("Inside get query data")
    if hasattr(query_statement, "statement"):
        query_str = str(query_statement.statement.compile(dialect=postgresql.dialect()))
        print(query_str)
        query = query_str.replace("\"", "").replace("\n", "").replace("\\", "")
        print(query)
    else:
        query = str(query_statement)
    print(f"Running Query:\n{query}")
    with db_engine.connect() as con:
        result_set = con.execute(text(query))
        result = result_set.fetchall()
    return result
