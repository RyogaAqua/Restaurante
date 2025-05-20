from flask import Flask, send_from_directory, jsonify, render_template, request
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
from Logica.app.routes.menu_routes import menu_routes
from Logica.app.routes.cart_routes import bp as cart_bp  # Importar el blueprint con el nombre correcto
from Logica.app.routes.auth_routes import auth_bp
from Logica.app.routes.point_store_routes import bp as point_store_bp
import os
import logging
import traceback
from flask.cli import with_appcontext
from flask_login import LoginManager

# Configurar logging detallado para Werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Asegurarse de que Werkzeug registre las solicitudes HTTP
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cambiar el nivel de logging a WARNING para reducir la verbosidad
logging.getLogger().setLevel(logging.WARNING)

# Registrar un mensaje al iniciar el servidor
logging.info("Werkzeug logging configurado para registrar solicitudes HTTP.")

migrate = Migrate()
login_manager = LoginManager()

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
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'template_folder', 'templates')
    )
    app.config.from_object(Config)

    # Inicializa las extensiones
    migrate.init_app(app, db)  # Registrar Flask-Migrate con la aplicación y la base de datos
    cors.init_app(app, resources={r"/*": {"origins": "*"}})  # Permitir todas las solicitudes de origen cruzado

    # Initialize the database
    db.init_app(app)

    # Configurar LoginManager
    login_manager.login_view = 'auth.login'  # Ruta para la página de inicio de sesión
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.init_app(app)  # Inicializar LoginManager con la aplicación Flask

    # Registra los blueprints usando la función register_routes
    register_routes(app)

    # Registrar el blueprint de rutas del menú
    app.register_blueprint(menu_routes, url_prefix='/menu')

    # Registrar el blueprint del carrito con el prefijo correcto
    logging.debug("Registrando el Blueprint cart_bp con prefijo '/api/cart'")
    app.register_blueprint(cart_bp, url_prefix='/api/cart', name='cart_blueprint')

    # Registrar el blueprint de autenticación con un prefijo explícito
    logging.debug("Registrando el Blueprint auth_bp con prefijo '/auth'")
    app.register_blueprint(auth_bp, url_prefix='/auth', name='auth_blueprint')

    # Registrar el blueprint de point_store_routes
    app.register_blueprint(point_store_bp)

    # Agrega manejadores globales de errores
    register_error_handlers(app)

    # Registrar un manejador para capturar todas las solicitudes entrantes
    @app.before_request
    def log_request_info():
        logging.debug(f"Solicitud entrante: {request.method} {request.url}")

    # Registrar un manejador para listar todas las rutas registradas al inicio
    for rule in app.url_map.iter_rules():
        logging.debug(f"Ruta registrada: {rule}")

    # Ruta para servir la página principal
    @app.route("/")
    def home():
        return render_template('index.html')

    # Ruta explícita para la página de registro
    @app.route("/signup")
    def signup():
        return render_template('signup.html')

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

# Definir la función de carga de usuarios
@login_manager.user_loader
def load_user(user_id):
    from .models import Usuarios  # Importar el modelo de usuario
    return Usuarios.query.get(int(user_id))

# Asegúrate de que Flask CLI pueda reconocer el contexto de la aplicación
app = create_app()

# Exponer el objeto `app` para Flask CLI
if __name__ == "__main__":
    app.run(debug=True)
