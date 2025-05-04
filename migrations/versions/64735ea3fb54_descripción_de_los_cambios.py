"""Descripción de los cambios

Revision ID: 64735ea3fb54
Revises: fb53e30d0480
Create Date: 2025-05-03 22:27:18.683806

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '64735ea3fb54'
down_revision = 'fb53e30d0480'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Asegúrate de que no se intente eliminar ninguna tabla fundamental
    tablas_protegidas = [
        'address',
        'menu_objetos',
        'orden',
        'orden_items',
        'puntos_balance',
        'usuarios'
    ]

    for tabla in tablas_protegidas:
        if conn.dialect.has_table(conn, tabla):
            print(f"La tabla '{tabla}' está protegida y no será eliminada.")

    # Si hay operaciones adicionales que no impliquen eliminar tablas, agrégalas aquí


def downgrade():
    conn = op.get_bind()

    # Asegúrate de que no se intente recrear tablas fundamentales innecesariamente
    tablas_protegidas = [
        'address',
        'menu_objetos',
        'orden',
        'orden_items',
        'puntos_balance',
        'usuarios'
    ]

    for tabla in tablas_protegidas:
        if conn.dialect.has_table(conn, tabla):
            print(f"La tabla '{tabla}' está protegida y no será recreada.")

    # Si hay operaciones adicionales que no impliquen recrear tablas, agrégalas aquí
