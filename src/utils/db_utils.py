from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from utils.config_utils import get_db_config
import logging

logger = logging.getLogger(__name__)

def connection():
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
    except Exception as e:
        logger.error(f"Error executing SQL file {sql_file_path}: {e}", exc_info=True)
        raise

def get_result_from_query(query_statement: str, db: Session):
    try:
        result = db.execute(text(query_statement)).fetchall()
        return result
    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")
