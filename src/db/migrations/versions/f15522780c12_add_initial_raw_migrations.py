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

"""Add initial raw migrations

Revision ID: f15522780c12
Revises: None
Create Date: 2024-09-17 13:16:39.120221

"""
from alembic import op
import os
import sqlalchemy as sa

# Define the revision identifiers, used by Alembic.
revision = 'f15522780c12'
down_revision = None  # Change this if it's not the first migration
branch_labels = None
depends_on = None

# Directory containing your SQL files
SQL_MIGRATIONS_DIR = 'sql/'

def get_sql_files(directory):
    """Retrieve SQL files from the directory sorted by filename."""
    files = [f for f in os.listdir(directory) if f.endswith('.sql')]
    files.sort()  # Ensure the files are applied in a sorted order
    return files

def execute_sql_file(file_path):
    """Execute a single SQL file."""
    with open(file_path, 'r') as file:
        sql = file.read()
    print(f'Executing SQL file: {file_path}')
    op.execute(sql)

def upgrade():
    """Apply new SQL migrations."""
    # Create an applied_migrations table if it does not exist
    create_applied_migrations_table()

    # Get the list of applied migrations
    applied_files = get_applied_migrations()

    # Get the list of SQL files in the directory
    sql_files = get_sql_files(SQL_MIGRATIONS_DIR)

    for sql_file in sql_files:
        if sql_file not in applied_files:
            file_path = os.path.join(SQL_MIGRATIONS_DIR, sql_file)
            execute_sql_file(file_path)
            record_applied_migration(sql_file)
            print(f'Successfully applied migration: {sql_file}')

def downgrade():
    """Handle downgrades by reversing SQL commands."""
    # Implement downgrade logic if necessary
    pass

def create_applied_migrations_table():
    """Create the applied_migrations table if it doesn't exist."""
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, 'applied_migrations'):
        op.create_table(
            'applied_migrations',
            sa.Column('file_name', sa.String(), nullable=False, primary_key=True),
            sa.Column('applied_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
        )

def get_applied_migrations():
    """Retrieve the list of applied migrations from the database."""
    conn = op.get_bind()
    result = conn.execute(sa.text('SELECT file_name FROM applied_migrations'))
    return {row['file_name'] for row in result}

def record_applied_migration(file_name):
    """Record a migration as applied in the database."""
    conn = op.get_bind()
    conn.execute(
        sa.text('INSERT INTO applied_migrations (file_name) VALUES (:file_name)'),
        {'file_name': file_name}
    )


upgrade()
