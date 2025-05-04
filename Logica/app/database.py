# Importa la biblioteca os para manejar variables de entorno.
import os

# Importa la clase SQLAlchemy de la biblioteca Flask-SQLAlchemy.
# Esta biblioteca se utiliza para integrar SQLAlchemy con aplicaciones Flask.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

# Define Base como db.Model para que los modelos puedan usarlo
Base = db.Model

# Configuración de la base de datos MySQL
DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:2016@localhost/mydb')

# Crea el motor y la sesión
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Función de ejemplo para probar la conexión
def test_connection():
    try:
        connection = engine.connect()
        print("Connection to MySQL database was successful!")
        connection.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Llama a test_connection para verificar
test_connection()
