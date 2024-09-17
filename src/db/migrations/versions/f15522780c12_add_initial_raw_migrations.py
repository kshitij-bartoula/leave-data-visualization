# """Add initial raw migrations

# Revision ID: f15522780c12
# Revises:
# Create Date: 2024-09-17 13:16:39.120221

# """
# from alembic import op
# import os

# # Define the revision identifiers, used by Alembic.
# revision = 'f15522780c12'
# down_revision = None  # Change this if it's not the first migration
# branch_labels = None
# depends_on = None

# # Directory containing your SQL files
# SQL_MIGRATIONS_DIR = 'sql/'

# def get_sql_files(directory):
#     """Retrieve SQL files from the directory sorted by filename."""
#     files = [f for f in os.listdir(directory) if f.endswith('.sql')]
#     files.sort()  # Ensure the files are applied in a sorted order
#     return files

# def execute_sql_file(file_path):
#     """Execute a single SQL file."""
#     with open(file_path, 'r') as file:
#         sql = file.read()
#     print('sql file path:', file_path)
#     op.execute(sql)

# def upgrade():
#     """Apply all SQL migrations."""
#     sql_files = get_sql_files(SQL_MIGRATIONS_DIR)

#     for sql_file in sql_files:
#         file_path = os.path.join(SQL_MIGRATIONS_DIR, sql_file)
#         execute_sql_file(file_path)
#         print('migrations has been successfully completed for: ', sql_file)

# def downgrade():
#     """Handle downgrades by reversing SQL commands.
#     For simplicity, we assume all commands are reversible or can be manually handled.
#     """
#     # Example of downgrades – you should implement actual downgrade logic or SQL files
#     pass

# upgrade()

"""Add new SQL migration

Revision ID: f15522780c12
Revises:
Create Date: 2024-09-17 13:16:39.120221

"""
from alembic import op
import os
from sqlalchemy import text

# Define the revision identifiers, used by Alembic.
revision = 'f15522780c12'
down_revision = None  # Change this if it's not the first migration
branch_labels = None
depends_on = None

# Directory containing your SQL files
SQL_MIGRATIONS_DIR = 'sql/'
APPLIED_MIGRATIONS_TABLE = 'applied_migrations'

def get_sql_files(directory):
    """Retrieve SQL files from the directory sorted by filename."""
    files = [f for f in os.listdir(directory) if f.endswith('.sql')]
    files.sort()  # Ensure the files are applied in a sorted order
    return files

def get_applied_migrations():
    """Retrieve the list of already applied migrations."""
    conn = op.get_bind()  # Get the connection directly
    query = text(f"SELECT filename FROM {APPLIED_MIGRATIONS_TABLE}")
    result = conn.execute(query)
    applied_files = {row[0] for row in result}
    return applied_files

def mark_as_applied(file_name):
    """Mark a migration file as applied."""
    conn = op.get_bind()  # Get the connection directly
    query = text(f"INSERT INTO {APPLIED_MIGRATIONS_TABLE} (filename) VALUES (:filename)")
    conn.execute(query, {'filename': file_name})

def execute_sql_file(file_path):
    """Execute a single SQL file."""
    with open(file_path, 'r') as file:
        sql = file.read()
    try:
        op.execute(text(sql))  # Ensure the SQL is wrapped in text() for execution
        print(f'Executed SQL file: {file_path}')
    except Exception as e:
        print(f'Error executing SQL file {file_path}: {e}')
        raise

def upgrade():
    """Apply new SQL migrations."""
    applied_files = get_applied_migrations()
    sql_files = get_sql_files(SQL_MIGRATIONS_DIR)

    for sql_file in sql_files:
        if sql_file not in applied_files:
            file_path = os.path.join(SQL_MIGRATIONS_DIR, sql_file)
            execute_sql_file(file_path)
            mark_as_applied(sql_file)
            print(f'Migration successfully applied: {sql_file}')
        else:
            print(f'Skipping already applied migration: {sql_file}')


def downgrade():
    """Handle downgrades by reversing SQL commands."""
    # Implement downgrade logic or provide SQL files as needed
    pass

upgrade()
