"""Add new SQL migration

Revision ID: f15522780c12
Revises:
Create Date: 2024-09-17 13:16:39.120221

"""
from alembic import op
import os
from sqlalchemy import text

# Auto-detect migration script
# This file is automatically created by Alembic and acts as a version control marker

revision = 'f15522780c12'
down_revision = None  # Set this to the previous revision or None for the first migration
branch_labels = None
depends_on = None

def upgrade():
    # In this setup, the env.py handles the SQL file execution
    # No need to include anything here if you use auto-detection in env.py
    pass

def downgrade():
    # If you need to manually handle downgrades (which can be tricky with raw SQL files)
    # This could include logic to roll back changes in reverse order.
    pass
