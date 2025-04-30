# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Asegúrate de que flask-cors esté instalado
from flask_wtf import CSRFProtect

# Instancia de SQLAlchemy para manejar la base de datos
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()  # Inicializa CORS
csrf = CSRFProtect()