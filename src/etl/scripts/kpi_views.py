
from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_kpi_views(db_engine):
    sql_file_path = Path("../db/etl_process/kpi_views.sql")
    logger.info(f"SQL file path for creating KPI views: {sql_file_path}")
    execute_sql_from_file(sql_file_path, db_engine)
    logger.info("KPI views created successfully.")

def refresh_kpi_views(db_engine):
    sql_file_path = Path("../db/etl_process/refresh_kpi_views.sql")
    logger.info(f"SQL file path for refreshing KPI views: {sql_file_path}")
    execute_sql_from_file(sql_file_path, db_engine)
    logger.info("KPI views refreshed successfully.")

def main():
    db_engine = connection()

    create_kpi_views(db_engine)
    refresh_kpi_views(db_engine)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
