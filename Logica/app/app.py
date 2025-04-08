from flask import Flask
from flask_migrate import Migrate
from .database import db  # Importa la instancia de SQLAlchemy desde database.py
from .config import Config  # Importa la configuración
from .routes import bp as routes_bp  # Importa el blueprint principal para las rutas

# Crea una instancia de Migrate para gestionar migraciones de base de datos.
migrate = Migrate()

# Función para crear y configurar la aplicación Flask.
def create_app():
    # Crea una instancia de la aplicación Flask.
    app = Flask(__name__)
    # Carga la configuración desde la clase Config.
    app.config.from_object(Config)

    # Inicializa las extensiones.
    db.init_app(app)  # Configura la base de datos con la aplicación.
    migrate.init_app(app, db)  # Configura Flask-Migrate con la aplicación y la base de datos.

    # Registra los blueprints.
    app.register_blueprint(routes_bp)  # Registra las rutas principales.

    # Agrega manejadores globales de errores (opcional).
    register_error_handlers(app)

    # Devuelve la instancia de la aplicación configurada.
    return app

# Manejadores globales de errores (opcional).
def register_error_handlers(app):
    # Maneja errores 404 (recurso no encontrado).
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Recurso no encontrado"}, 404

    # Maneja errores 500 (error interno del servidor).
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Ocurrió un error interno"}, 500
