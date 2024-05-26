from utils.db_utils import connection, execute_sql_from_file
from pathlib import Path
from sqlalchemy.sql import text

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

with db_engine.connect() as conn:
    schema_existence_query = text(
        "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'dw')"
    )
    schema_exists = conn.execute(schema_existence_query).scalar()
    print(schema_exists)

    if not schema_exists:
        print('Schema does not exist. Creating schema...')
        create_schema_query = text(
        "BEGIN; CREATE SCHEMA dw; COMMIT;"
        )
        create_schema = conn.execute(create_schema_query)
        print('dw schema created')
    else:
        print('Schema already exists')

create_tables(db_engine)
insert_in_tables(db_engine)
