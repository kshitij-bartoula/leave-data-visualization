from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def insert_in_tables(db_engine):
    sql_file_path = Path("/app/etl/scripts/sql/insert.sql")
    try:
        execute_sql_from_file(sql_file_path, db_engine)
    except Exception as e:
        logger.error("Insert SQL execution failed", exc_info=True)
        raise

def main():
    insert_in_tables(connection())
