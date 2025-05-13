from flask import Flask, render_template
import logging

"""
Este módulo inicializa y registra los blueprints para las rutas de la aplicación Flask.

Los blueprints permiten organizar las rutas en módulos separados, facilitando
la escalabilidad y el mantenimiento del código.
"""

# Importa los blueprints de las rutas
from .address_routes import bp as address_bp
from .auth_routes import auth_bp
from .delivery_routes import bp as delivery_bp
from .cart_routes import bp as cart_bp
from .inventory_routes import bp as inventory_bp
from .menu_routes import bp as menu_bp
from .notification_routes import bp as notification_bp
from .order_routes import bp as order_bp
from .payment_routes import bp as payment_bp
from .reward_routes import bp as reward_bp
from .support_routes import bp as support_bp
from .stats_routes import bp as stats_bp

def register_routes(app: Flask):
    """Registra todos los blueprints en la aplicación Flask."""
    # Ruta para la página principal
    @app.route('/')
    def home_page():
        return render_template('index.html')

    # Otra ruta con un endpoint diferente
    @app.route('/about')
    def about_page():
        return render_template('about.html')

    app.register_blueprint(address_bp, url_prefix='/addresses')
    logging.info("Registering auth_bp blueprint with prefix '/auth'")
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Asegúrate de registrar el blueprint de autenticación
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    # app.register_blueprint(cart_bp, url_prefix='/cart')  # Eliminado para evitar duplicados
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(notification_bp, url_prefix='/notifications')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(reward_bp, url_prefix='/rewards')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(stats_bp, url_prefix='/stats')

    # Manejar error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404