# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\tests\test_db_connection.py
import sys
import os
from sqlalchemy.sql import text  # Importa text para consultas SQL

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    try:
        # Ejecuta una consulta básica para verificar la conexión
        db.session.execute(text('SELECT 1'))
        print("Conexión exitosa a la base de datos.")

        # Verifica si puedes acceder a una tabla específica
        result = db.session.execute('SELECT * FROM Usuarios LIMIT 1').fetchall()
        if result:
            print("Acceso exitoso a la tabla 'Usuarios'. Datos de ejemplo:", result)
        else:
            print("La tabla 'Usuarios' está vacía, pero la conexión es exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos o consultar la tabla: {e}")
    finally:
        db.session.remove()

def test_db_connection():
    """
    Prueba básica para verificar la conexión a la base de datos.
    """
    with app.app_context():
        try:
            # Usa text() para envolver la consulta SQL
            db.session.execute(text('SELECT 1'))
            assert True, "Conexión exitosa a la base de datos."
        except Exception as e:
            assert False, f"Error al conectar a la base de datos: {e}"