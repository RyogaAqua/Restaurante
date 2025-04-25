from flask import Flask
from flask_migrate import Migrate
from .extensions import db
from .config import Config
from .routes import bp as routes_bp

migrate = Migrate()

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.

    - Configura la aplicación utilizando la clase Config.
    - Inicializa las extensiones como la base de datos y Flask-Migrate.
    - Registra los blueprints para manejar las rutas.
    - Agrega manejadores globales de errores.

    Returns:
        app (Flask): La instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)  # Inicializa Flask-Migrate

    # Registra los blueprints
    app.register_blueprint(routes_bp)

    # Agrega manejadores globales de errores (opcional)
    register_error_handlers(app)

    return app

# Manejadores globales de errores (opcional)
def register_error_handlers(app):
    """
    Registra manejadores globales de errores para la aplicación.

    - Maneja errores 404 (Recurso no encontrado).
    - Maneja errores 500 (Error interno del servidor).

    Args:
        app (Flask): La instancia de la aplicación Flask.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Maneja errores 404.

        Args:
            error: El error capturado.

        Returns:
            dict: Un mensaje de error en formato JSON.
            int: Código de estado HTTP 404.
        """
        return {"error": "Recurso no encontrado"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Maneja errores 500.

        Args:
            error: El error capturado.

        Returns:
            dict: Un mensaje de error en formato JSON.
            int: Código de estado HTTP 500.
        """
        return {"error": "Ocurrió un error interno"}, 500

