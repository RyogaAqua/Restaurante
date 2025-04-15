# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\tests\test_db_connection.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")