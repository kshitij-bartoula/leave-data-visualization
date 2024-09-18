"""Add new SQL migration

Revision ID: f15522780c12
Revises:
Create Date: 2024-09-17 13:16:39.120221

"""
from alembic import op
import os
from sqlalchemy import text


revision = 'f15522780c12'
down_revision = None  # Set this to the previous revision or None for the first migration
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
