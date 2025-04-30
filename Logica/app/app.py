from flask import Flask, send_from_directory, jsonify, render_template
from flask_migrate import Migrate
from .extensions import db, cors
from .config import Config
from .routes import bp as routes_bp
from Logica.app.routes import (
    address_routes,
    auth_routes,
    delivery_routes,
    cart_routes,
    inventory_routes,
    menu_routes,
    notification_routes,
    order_routes,
    payment_routes,
    reward_routes,
    support_routes,
    stats_routes,
)
import os

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
    app = Flask(
        __name__,
        static_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2'),
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2')
    )
    app.config.from_object(Config)

    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)  # Inicializa Flask-Migrate
    cors.init_app(app, resources={r"/*": {"origins": "*"}})  # Permitir todas las solicitudes de origen cruzado

    # Registra los blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(address_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(delivery_routes.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(inventory_routes.bp)
    app.register_blueprint(menu_routes.bp)
    app.register_blueprint(notification_routes.bp)
    app.register_blueprint(order_routes.bp)
    app.register_blueprint(payment_routes.bp)
    app.register_blueprint(reward_routes.bp)
    app.register_blueprint(support_routes.bp)
    app.register_blueprint(stats_routes.bp)

    # Agrega manejadores globales de errores
    register_error_handlers(app)

    # Ruta para servir la página principal
    @app.route("/")
    def home():
        return app.send_static_file('index.html')

    # Ruta para servir archivos estáticos (CSS, JS, imágenes, etc.)
    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    return app

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

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
