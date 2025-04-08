# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\extensions.py
from flask_sqlalchemy import SQLAlchemy  # Importa SQLAlchemy para manejar la base de datos

# Inicializa la instancia de SQLAlchemy
# Esta instancia será utilizada para interactuar con la base de datos en toda la aplicación
db = SQLAlchemy()