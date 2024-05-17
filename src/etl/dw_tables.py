from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path

def create_tables(db_engine):
    sql_file_path = Path("/app/db/create_tables.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)

def insert_in_tables(db_engine):
    sql_file_path = Path("/app/db/insert.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)

db_engine = connection()

create_tables(db_engine)
insert_in_tables(db_engine)
