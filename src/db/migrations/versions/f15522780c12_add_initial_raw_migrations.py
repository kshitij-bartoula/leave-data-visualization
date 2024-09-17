"""Add initial raw migrations

Revision ID: f15522780c12
Revises:
Create Date: 2024-09-17 13:16:39.120221

"""
from alembic import op
import os

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
    op.execute(sql)

def upgrade():
    """Apply all SQL migrations."""
    sql_files = get_sql_files(SQL_MIGRATIONS_DIR)
    for sql_file in sql_files:
        file_path = os.path.join(SQL_MIGRATIONS_DIR, sql_file)
        execute_sql_file(file_path)

def downgrade():
    """Handle downgrades by reversing SQL commands.
    For simplicity, we assume all commands are reversible or can be manually handled.
    """
    # Example of downgrades – you should implement actual downgrade logic or SQL files
    pass
