from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_kpi_views(db_engine):
    try:
        execute_sql_from_file(Path("/app/etl/scripts/sql/kpi_views.sql"), db_engine)
    except Exception as e:
        logger.error("Creating KPI views failed", exc_info=True)
        raise

def refresh_kpi_views(db_engine):
    try:
        execute_sql_from_file(Path("/app/etl/scripts/sql/refresh_kpi_views.sql"), db_engine)
    except Exception as e:
        logger.error("Refreshing KPI views failed", exc_info=True)
        raise

def main():
    db_engine = connection()
    create_kpi_views(db_engine)
    refresh_kpi_views(db_engine)
