
from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
from sqlalchemy.sql import text
import logging

logger = logging.getLogger(__name__)

def insert_in_tables(db_engine):
    sql_file_path = Path("/app/db/etl_process/insert.sql")
    logger.info(f"SQL file path for inserting data: {sql_file_path}")
    execute_sql_from_file(sql_file_path, db_engine)
    logger.info("Data inserted into tables successfully.")

def main():
    db_engine = connection()
    insert_in_tables(db_engine)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
