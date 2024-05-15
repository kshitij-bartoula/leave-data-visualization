from utils.db_utils import connection, execute_sql_from_file
from sqlalchemy.sql import text
from pathlib import Path
from sqlalchemy import create_engine


def create_tables(db_engine):
    sql_file_path = Path("../db/create_tables.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)

def insert_in_tables(db_engine):
    sql_file_path = Path("../db/insert.sql")
    print(sql_file_path)
    print(db_engine)
    execute_sql_from_file(sql_file_path, db_engine)


db_engine = connection()

create_tables(db_engine)
insert_in_tables(db_engine)
