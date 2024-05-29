from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path

def create_kpi_views(db_engine):
    sql_file_path = Path("/app/db/kpi_views.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)

def refresh_kpi_views(db_engine):
    sql_file_path = Path("/app/db/refresh_kpi_views.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)

def main():
    db_engine = connection()

    create_kpi_views(db_engine)
    refresh_kpi_views(db_engine)

if __name__ == "__main__":
    main()