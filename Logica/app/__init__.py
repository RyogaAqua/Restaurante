import os
from flask import Flask, render_template
from flask_migrate import Migrate
from .extensions import db
from .routes.auth_routes import auth_bp  # Importar el blueprint de autenticación

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
    # Configura Flask para usar PaginaWeb2 como base para plantillas y archivos estáticos
    app = Flask(
        __name__,
        static_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2', 'static'),
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2')
    )

    # Load configuration
    app.config.from_object('Logica.app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar el blueprint de autenticación
    app.register_blueprint(auth_bp)

    # Ruta para la página principal
    @app.route('/')
    def home():
        return render_template('index.html')  # Usa render_template para buscar en template_folder

    # Ruta genérica para servir otras páginas HTML
    @app.route('/<page_name>.html')
    def render_page(page_name):
        return render_template(f"{page_name}.html")  # Busca en template_folder

    return app

