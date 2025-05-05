from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.config_utils import get_db_config
from sqlalchemy import create_engine


def connection():
    """
    Create a database engine using credentials from config.
    Only used once in database.py.
    """
    db_config = get_db_config()
    DB_USERNAME = db_config['DB_USERNAME']
    DB_PASSWORD = db_config['DB_PASSWORD']
    DB_HOST = db_config['DB_HOST']
    DB_NAME = db_config['DB_NAME']

    if all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
        DB_CONNECTION_STR = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
        return create_engine(DB_CONNECTION_STR)
    else:
        raise ValueError("Missing DB connection variables in environment.")


def execute_sql_from_file(sql_file_path, db_engine):
    try:
        with db_engine.connect() as con:
            with open(sql_file_path, 'r') as sql_file:
                query = text(sql_file.read())
                con.execute(query)
        print(f"SQL from file executed successfully")
    except Exception as e:
        print(f"Error executing SQL from file: {e}")


def get_result_from_query(query_statement: str, db: Session):
    """
    Executes a SQL SELECT query using an existing SQLAlchemy session.
    """
    try:
        result = db.execute(text(query_statement)).fetchall()
        return result
    except Exception as e:
        print(f"Query failed: {e}")
        return []