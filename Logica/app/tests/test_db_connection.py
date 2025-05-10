# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\tests\test_db_connection.py
import sys
import os
from sqlalchemy.sql import text  # Importa text para consultas SQL
import pytest

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Logica.app.main import create_app
from app.extensions import db

def test_db_connection():
    """
    Prueba básica para verificar la conexión a la base de datos.
    """
    app = create_app()  # Crea la aplicación usando la función create_app

    with app.app_context():
        try:
            # Usa text() para envolver la consulta SQL
            db.session.execute(text('SELECT 1'))
            assert True, "Conexión exitosa a la base de datos."
        except Exception as e:
            assert False, f"Error al conectar a la base de datos: {e}"