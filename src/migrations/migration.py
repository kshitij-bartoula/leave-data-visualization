# import os
# from alembic import context
# from sqlalchemy import create_engine, pool, text
# from logging.config import fileConfig

# config = context.config
# fileConfig(config.config_file_name)

# #'autogenerate' if needed.
# target_metadata = None

# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# SQL_FOLDER = 'sql'

# def run_migrations_offline():
#     """Run migrations in 'offline' mode."""
#     url = SQLALCHEMY_DATABASE_URL
#     context.configure(url=url, literal_binds=True)

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online():
#     """Run migrations in 'online' mode."""
#     connectable = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

#     with connectable.connect() as connection:
#         context.configure(connection=connection)

#         connection.execute(text("""
#             CREATE TABLE IF NOT EXISTS migration_history (
#                 id SERIAL PRIMARY KEY,
#                 migration_name VARCHAR(255) UNIQUE NOT NULL,
#                 applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );
#         """))

#         #transaction
#         with context.begin_transaction():
#             sql_files = sorted([f for f in os.listdir(SQL_FOLDER) if f.endswith('.sql')])

#             for sql_file in sql_files:
#                 result = connection.execute(
#                     text("SELECT migration_name FROM migration_history WHERE migration_name = :name"),
#                     {"name": sql_file}
#                 ).fetchone()

#                 if result:
#                     print(f"Skipping already applied migration: {sql_file}")
#                     continue

#                 # Read and execute each SQL file
#                 sql_path = os.path.join(SQL_FOLDER, sql_file)
#                 with open(sql_path, 'r') as file:
#                     sql_command = file.read()
#                     print(f"Running new SQL migration: {sql_file}")
#                     connection.execute(text(sql_command))

#                 # Record migration in the migration_history table
#                 connection.execute(
#                     text("INSERT INTO migration_history (migration_name) VALUES (:name)"),
#                     {"name": sql_file}
#                 )

#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SQL_FOLDER = 'sql'

# Create the database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

def run_migrations():
    """Run migrations from the SQL folder."""
    with engine.connect() as connection:
        # Ensure migration_history table exists
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS migration_history_new (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Get the list of all SQL files in the migration folder
        sql_files = sorted([f for f in os.listdir(SQL_FOLDER) if f.endswith('.sql')])

        for sql_file in sql_files:
            # Check if the migration has already been applied
            result = connection.execute(
                text("SELECT migration_name FROM migration_history WHERE migration_name = :name"),
                {"name": sql_file}
            ).fetchone()

            if result:
                print(f"Skipping already applied migration: {sql_file}")
                continue

            # Read and execute the SQL file
            sql_path = os.path.join(SQL_FOLDER, sql_file)
            with open(sql_path, 'r') as file:
                sql_command = file.read()
                print(f"Running new SQL migration: {sql_file}")
                connection.execute(text(sql_command))

            # Record the applied migration in the migration_history table
            connection.execute(
                text("INSERT INTO migration_history (migration_name) VALUES (:name)"),
                {"name": sql_file}
            )

if __name__ == "__main__":
    run_migrations()