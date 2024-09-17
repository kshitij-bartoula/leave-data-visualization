
from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
from sqlalchemy.sql import text
import logging

logger = logging.getLogger(__name__)

# def create_tables(db_engine):
#     sql_file_path = Path("/app/db/create_tables.sql")
#     logger.info(f"SQL file path for creating tables: {sql_file_path}")
#     execute_sql_from_file(sql_file_path, db_engine)
#     logger.info("Tables created successfully.")

def insert_in_tables(db_engine):
    sql_file_path = Path("/app/db/etl_process/insert.sql")
    logger.info(f"SQL file path for inserting data: {sql_file_path}")
    execute_sql_from_file(sql_file_path, db_engine)
    logger.info("Data inserted into tables successfully.")

def main():
    db_engine = connection()

    with db_engine.connect() as conn:
        schema_existence_query = text(
            "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'dw')"
        )
        schema_exists = conn.execute(schema_existence_query).scalar()
        logger.info(f"Schema 'dw' existence check: {schema_exists}")

        if not schema_exists:
            logger.info('Schema does not exist. Creating schema...')
            create_schema_query = text(
                "BEGIN; CREATE SCHEMA dw; COMMIT;"
            )
            create_schema = conn.execute(create_schema_query)
            logger.info('Schema "dw" created successfully.')
        else:
            logger.info('Schema "dw" already exists.')

    insert_in_tables(db_engine)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
