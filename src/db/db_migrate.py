
import os
import logging
from ...utils.db_utils import connection
from sqlalchemy import text
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

SQL_FOLDER = 'sql'

def get_db_connection():
    return connection()

def migration_down():
    """Perform rollback migrations."""
    schemas = ["raw", "dw"]
    db_engine = get_db_connection()

    with db_engine.connect() as conn:
        with conn.begin():
            for schema in schemas:
                query = text("DROP SCHEMA IF EXISTS :schema_name CASCADE;")
                conn.execute(query, {"schema_name": schema})
            logger.info("[+] VyagutaInfo Database cleaned!\n")

def migration_up():
    """Perform migrations up."""
    db_engine = get_db_connection()

    with db_engine.connect() as conn:
        with conn.begin():  # Ensure transaction
            # Ensure migration_history table exists
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS migration_history (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(255) UNIQUE NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_latest BOOLEAN DEFAULT FALSE
                );
            """))

            # Process .up.sql files
            sql_files = sorted([f for f in os.listdir(SQL_FOLDER) if f.endswith('.up.sql')])
            for sql_file in sql_files:
                result = conn.execute(
                    text("SELECT migration_name FROM migration_history WHERE migration_name = :name"),
                    {"name": sql_file}
                ).fetchone()

                if result:
                    logger.info(f"Skipping already applied migration: {sql_file}")
                    continue

                # Read and execute each SQL file
                sql_path = os.path.join(SQL_FOLDER, sql_file)
                with open(sql_path, 'r') as f:
                    sql_command = f.read()
                conn.execute(text(sql_command))
                logger.info(f"[+] Executed {sql_file}")

                # Record migration in the migration_history table
                conn.execute(
                    text("INSERT INTO migration_history (migration_name, is_latest) VALUES (:name, TRUE)"),
                    {"name": sql_file}
                )

                # Set all previous migrations to not latest
                conn.execute(
                    text("UPDATE migration_history SET is_latest = FALSE WHERE migration_name != :name"),
                    {"name": sql_file}
                )

def rollback_migration():
    """Roll back the latest migration."""
    db_engine = get_db_connection()

    with db_engine.connect() as conn:
        # Find the migration to rollback
        migrations_to_rollback = conn.execute(
            text("SELECT migration_name FROM migration_history WHERE is_latest = FALSE")
        ).fetchall()

        if not migrations_to_rollback:
            logger.info("No migrations to rollback.")
            return

        for migration in migrations_to_rollback:
            migration_name = migration[0]
            down_sql_file = migration_name.replace('.up.sql', '.down.sql')
            down_sql_path = os.path.join(SQL_FOLDER, down_sql_file)

            if os.path.isfile(down_sql_path):
                with open(down_sql_path, 'r') as f:
                    down_sql_command = f.read()
                conn.execute(text(down_sql_command))
                logger.info(f"Rolled back migration: {migration_name}")

                # Remove the rollback migration from history
                conn.execute(
                    text("DELETE FROM migration_history WHERE migration_name = :name"),
                    {"name": migration_name}
                )
            else:
                logger.error(f"No rollback file found for {migration_name}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--up",
        action="store_true",
        help="Run migration_up for Vyaguta Leave Info tables.",
    )
    parser.add_argument(
        "--down",
        action="store_true",
        help="Run migration_down for Vyaguta Leave Info tables.",
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Run rollback_migration to revert migrations.",
    )
    args = parser.parse_args()

    if args.up:
        migration_up()
    elif args.down:
        migration_down()
    elif args.rollback:
        rollback_migration()

# import os
# import logging
# from utils.db_utils import connection
# from sqlalchemy.sql import text


# logger = logging.getLogger(__name__)


# def get_db_connection():
#     return connection()


# def migration_down():
#     schemas = ["raw", "dw"]
#     db_engine = get_db_connection()
#     with db_engine.connect() as conn:
#         for schema in schemas:
#             query = text("DROP SCHEMA IF EXISTS :schema_name CASCADE;")
#             conn.execute(query, {"schema_name": schema})
#     logger.info("[+] VyagutaInfo Database cleaned!\n")


# def migration_up():
#     db_engine = get_db_connection()

#     with db_engine.connect() as conn:
#         with conn.begin():  # Ensure transaction
#             directories = ["../db/migrations", "../db/sql"]
#             for directory in directories:
#                 if not os.path.exists(directory):
#                     logger.error(f"Directory {directory} does not exist")
#                     raise FileNotFoundError(f"Directory {directory} does not exist")

#                 for filename in sorted(os.listdir(directory)):
#                     if filename.endswith(".sql"):
#                         sql_file_path = os.path.join(directory, filename)
#                         try:
#                             with open(sql_file_path, "r") as f:
#                                 sql_command = f.read()

#                             conn.execute(sql_command)
#                             logger.info(f"[+] Executed {filename}")
#                             print(f"[+] Executed {filename}")

#                         except Exception as e:
#                             logger.error(f"[-] Failed to execute {filename}: {str(e)}")
#                             conn.rollback()  # Rollback in case of failure
#                             raise


# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--up",
#         action="store_true",
#         help="Run migration_up for Vyaguta Leave Info tables.",
#     )
#     parser.add_argument(
#         "--down",
#         action="store_true",
#         help="Run migration_down for Vyaguta Leave Info tables.",
#     )
#     args = parser.parse_args()

#     if args.up:
#         migration_up()
#     elif args.down:
#         migration_down()