# Importa la biblioteca os para manejar variables de entorno.
import os

# Importa la clase SQLAlchemy de la biblioteca Flask-SQLAlchemy.
# Esta biblioteca se utiliza para integrar SQLAlchemy con aplicaciones Flask.
from flask_sqlalchemy import SQLAlchemy

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

# Define Base como db.Model para que los modelos puedan usarlo
Base = db.Model

# Configuración de la base de datos MySQL
DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:2016@localhost/mydb')

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Usa únicamente la instancia de SQLAlchemy

# Función de ejemplo para probar la conexión
def test_connection():
    try:
        connection = db.engine.connect()
        print("Connection to MySQL database was successful!")
        connection.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Llama a test_connection para verificar
test_connection()