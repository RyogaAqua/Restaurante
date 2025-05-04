"""Renamed Address column to AddressLine

Revision ID: fb53e30d0480
Revises: 7f342c7f6f9f
Create Date: 2025-05-03 16:53:50.434319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fb53e30d0480'
down_revision = '7f342c7f6f9f'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('menu_objetos', schema=None) as batch_op:
        pass  # No hay índices que eliminar en esta tabla

    with op.batch_alter_table('orden', schema=None) as batch_op:
        pass  # No se realizan operaciones en esta tabla

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        pass  # No hay índices que eliminar en esta tabla

def downgrade():
    with op.batch_alter_table('menu_objetos', schema=None) as batch_op:
        pass  # Si no hay cambios necesarios, usa 'pass'

    op.create_table('menu_objetos',
    sa.Column('Objetos', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Nombre_Objeto', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Precio', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Categoria', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Calorias', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Restaurante', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['Restaurante'], ['restaurante.Id_Restaurante'], name='fk_Menu_Objetos_Restaurante1'),
    sa.PrimaryKeyConstraint('Objetos', 'Restaurante'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('menu_objetos', schema=None) as batch_op:
        batch_op.create_index('fk_Menu_Objetos_Restaurante1_idx', ['Restaurante'], unique=False)

    op.create_table('usuarios',
    sa.Column('Id_Usuario', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Nombre_Usuario', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Apellido_Usuario', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Email', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Telefono', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('Hash_Contrasena_Usuario', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('Fecha_Ingresada', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('MetodoDePago', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Puntos', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Address', mysql.VARCHAR(length=45), nullable=False),
    sa.ForeignKeyConstraint(['Address'], ['address.Address'], name='fk_Usuarios_Address1'),
    sa.PrimaryKeyConstraint('Id_Usuario', 'Puntos', 'Address'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.create_index('fk_Usuarios_Puntos1_idx', ['Puntos'], unique=False)
        batch_op.create_index('fk_Usuarios_Address1_idx', ['Address'], unique=False)
        batch_op.create_index('Telefono_UNIQUE', ['Telefono'], unique=True)
        batch_op.create_index('Hash_Contrasena_Usuario_UNIQUE', ['Hash_Contrasena_Usuario'], unique=True)
        batch_op.create_index('Email_UNIQUE', ['Email'], unique=True)

    op.create_table('puntos',
    sa.Column('PuntosTotal', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Redimidos', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Ofertas', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('PuntosGastados', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('PuntosTotal'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_table('address',
    sa.Column('Address', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Zip_code', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('State', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('Country', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('City', mysql.VARCHAR(length=45), nullable=True),
    sa.PrimaryKeyConstraint('Address'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_table('orden',
    sa.Column('Id_Transaccion', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Puntos_Total', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Precio_Total', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Id_Usuario', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Puntos', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Address', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('Objetos', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['Id_Usuario', 'Puntos', 'Address'], ['usuarios.Id_Usuario', 'usuarios.Puntos', 'usuarios.Address'], name='fk_Orden_Usuarios1'),
    sa.PrimaryKeyConstraint('Id_Transaccion', 'Id_Usuario', 'Puntos', 'Address', 'Objetos'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('orden', schema=None) as batch_op:
        batch_op.create_index('fk_Orden_Usuarios1_idx', ['Id_Usuario', 'Puntos', 'Address'], unique=False)

    op.create_table('restaurante',
    sa.Column('Id_Restaurante', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Restaurante_Address', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('Nombre', mysql.VARCHAR(length=45), nullable=True),
    sa.PrimaryKeyConstraint('Id_Restaurante'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
