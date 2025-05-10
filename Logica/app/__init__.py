import os
from flask import Flask, render_template
from flask_migrate import Migrate
from .extensions import db  # Ensure single instance of SQLAlchemy is used
from .routes.auth_routes import auth_bp  # Importar el blueprint de autenticación
from .database import init_app

# Initialize Flask-Migrate
migrate = Migrate()

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.

    - Configura la aplicación utilizando la clase Config.
    - Registra los blueprints para manejar las rutas.

    Returns:
        app (Flask): La instancia de la aplicación Flask configurada.
    """
    app = Flask(
        __name__,
        static_folder=os.path.join('..', '..', 'Pagina_Web', 'template_folder', 'static'),
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'template_folder', 'templates')
    )
    app.config.from_object('Logica.app.config.Config')

    # Initialize SQLAlchemy using the single instance
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)

    return app

