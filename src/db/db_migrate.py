# import os
# import argparse
# import sys

# import logging

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from utils.db_utils import connection, execute_sql_from_file
# from sqlalchemy.sql import text
# #from utils.logging import get_logger

# logger = logging.getLogger(__name__)


# def migration_down():
#     schemas = ["raw", "dw"]
#     #conn = connection()

#     db_engine = connection()
#     with db_engine.connect() as conn:
#         for schema in schemas:
#             query = text(
#                 "DROP SCHEMA IF EXISTS {schema} CASCADE;"
#             )
#             query = conn.execute(query).scalar()
#     logger.info("[+] VyagutaInfo Database cleaned!\n")


# def migration_up():
#     db_engine = connection()

#     # Start a transaction explicitly
#     with db_engine.connect() as conn:
#         with conn.begin():  # This ensures that all queries are part of a transaction
#             directories = ["../db/migrations", "../db/sql"]
#             for directory in directories:
#                 if not os.path.exists(directory):
#                     logger.error(f"Directory {directory} does not exist")
#                     continue

#                 for filename in sorted(os.listdir(directory)):
#                     if filename.endswith(".sql"):
#                         sql_file_path = os.path.join(directory, filename)
#                         try:
#                             with open(sql_file_path, "r") as f:
#                                 sql_command = f.read()

#                             # Execute the SQL command
#                             conn.execute(sql_command)
#                             logger.info(f"[+] Executed {filename}")
#                             print(f"[+] Executed {filename}")

#                         except Exception as e:
#                             # Error handling and rollback in case of failure
#                             logger.error(f"[-] Failed to execute {filename}: {str(e)}")
#                             raise  # Re-raise the exception to trigger rollback

# if __name__ == "__main__":
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

import os
import logging
from utils.db_utils import connection
from sqlalchemy.sql import text


logger = logging.getLogger(__name__)


def get_db_connection():
    return connection()


def migration_down():
    schemas = ["raw", "dw"]
    db_engine = get_db_connection()
    with db_engine.connect() as conn:
        for schema in schemas:
            query = text("DROP SCHEMA IF EXISTS :schema_name CASCADE;")
            conn.execute(query, {"schema_name": schema})
    logger.info("[+] VyagutaInfo Database cleaned!\n")


def migration_up():
    db_engine = get_db_connection()

    with db_engine.connect() as conn:
        with conn.begin():  # Ensure transaction
            directories = ["../db/migrations", "../db/sql"]
            for directory in directories:
                if not os.path.exists(directory):
                    logger.error(f"Directory {directory} does not exist")
                    raise FileNotFoundError(f"Directory {directory} does not exist")

                for filename in sorted(os.listdir(directory)):
                    if filename.endswith(".sql"):
                        sql_file_path = os.path.join(directory, filename)
                        try:
                            with open(sql_file_path, "r") as f:
                                sql_command = f.read()

                            conn.execute(sql_command)
                            logger.info(f"[+] Executed {filename}")
                            print(f"[+] Executed {filename}")

                        except Exception as e:
                            logger.error(f"[-] Failed to execute {filename}: {str(e)}")
                            conn.rollback()  # Rollback in case of failure
                            raise


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
    args = parser.parse_args()

    if args.up:
        migration_up()
    elif args.down:
        migration_down()

