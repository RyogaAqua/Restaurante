# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Instancia de SQLAlchemy para manejar la base de datos
db = SQLAlchemy()
cors = CORS()