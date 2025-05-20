"""Align models with MySQL schema

Revision ID: 7f342c7f6f9f
Revises: 
Create Date: 2025-05-03 13:26:08.058609

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '7f342c7f6f9f'
down_revision = None
branch_labels = None
depends_on = None


def foreign_key_exists(table_name, fk_name, connection):
    inspector = inspect(connection)
    foreign_keys = inspector.get_foreign_keys(table_name)
    return any(fk['name'] == fk_name for fk in foreign_keys)


# Added a function to check if a table exists before attempting to drop it.
def table_exists(table_name, connection):
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()


def upgrade():
    # Eliminar lógica que elimina tablas
    pass  # Asegurarse de que no se eliminen tablas en esta migración


def downgrade():
    # Eliminar lógica que elimina tablas
    pass  # Asegurarse de que no se eliminen tablas en esta migración
