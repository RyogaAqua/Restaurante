from flask import Flask, send_from_directory, jsonify, render_template
from flask_migrate import Migrate
from .extensions import cors, db  # Importar la instancia de SQLAlchemy
from .config import Config
from .routes import register_routes  # Importar la función para registrar rutas
from .routes import (
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
import logging
import traceback
from flask.cli import with_appcontext

# Configurar logging detallado para Werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Asegurarse de que Werkzeug registre las solicitudes HTTP
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Registrar un mensaje al iniciar el servidor
logging.info("Werkzeug logging configurado para registrar solicitudes HTTP.")

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
        static_folder=os.path.join('..', '..', 'Pagina_Web', 'template_folder', 'static'),
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'template_folder')
    )
    app.config.from_object(Config)

    # Inicializa las extensiones
    migrate.init_app(app, db)  # Registrar Flask-Migrate con la aplicación y la base de datos
    cors.init_app(app, resources={r"/*": {"origins": "*"}})  # Permitir todas las solicitudes de origen cruzado

    # Initialize the database
    db.init_app(app)

    # Registra los blueprints usando la función register_routes
    register_routes(app)

    # Agrega manejadores globales de errores
    register_error_handlers(app)

    # Ruta para servir la página principal
    @app.route("/")
    def home():
        return render_template('index.html')

    # Ruta genérica para servir otras páginas HTML
    @app.route("/<page_name>.html")
    def render_page(page_name):
        return render_template(f"{page_name}.html")  # Busca en template_folder

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
        logging.error(f"404 Error: {error}")
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
        logging.error(f"500 Error: {error}\n{traceback.format_exc()}")
        return {"error": "Ocurrió un error interno"}, 500

# Asegúrate de que Flask CLI pueda reconocer el contexto de la aplicación
app = create_app()

# Exponer el objeto `app` para Flask CLI
if __name__ == "__main__":
    app.run(debug=True)
