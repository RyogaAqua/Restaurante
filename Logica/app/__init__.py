import os
from flask import Flask, render_template
from flask_migrate import Migrate
from .extensions import db  # Ensure single instance of SQLAlchemy is used
from .routes.auth_routes import auth_bp  # Importar el blueprint de autenticación
from .database import init_app
from Logica.app.routes.cart_routes import bp as cart_bp
from .config import config_by_name  # Importar configuraciones por nombre
from .routes import register_routes  # Importar la función para registrar rutas

# Initialize Flask-Migrate
migrate = Migrate()

def create_app(config_name):
    """Crear y configurar la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones
    db.init_app(app)  # Asegurar que SQLAlchemy esté correctamente inicializado
    migrate.init_app(app, db)

    # Registrar blueprints
    register_routes(app)

    # Eliminar cualquier registro duplicado del blueprint `cart_bp`
    if 'cart_blueprint' in app.blueprints:
        del app.blueprints['cart_blueprint']

    # Registrar el blueprint del carrito con el prefijo correcto
    if 'cart' not in app.blueprints:
        app.register_blueprint(cart_bp, url_prefix='/api/cart')

    return app

