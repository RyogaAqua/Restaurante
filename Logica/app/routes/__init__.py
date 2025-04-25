from flask import Blueprint

"""
Este módulo inicializa y registra los blueprints para las rutas de la aplicación Flask.

Los blueprints permiten organizar las rutas en módulos separados, facilitando
la escalabilidad y el mantenimiento del código.
"""

# Crear un blueprint para el paquete de rutas
bp = Blueprint('routes', __name__)

# Importar y registrar blueprints individuales
from .auth_routes import bp as auth_bp  # Cambiar a import relativo
from .menu_routes import bp as menu_bp  # Cambiar a import relativo
from .order_routes import bp as order_bp  # Cambiar a import relativo
from .reward_routes import bp as reward_bp  # Cambiar a import relativo
from .payment_routes import bp as payment_bp  # Cambiar a import relativo

# Registrar los blueprints con el blueprint principal
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(menu_bp, url_prefix='/menu')
bp.register_blueprint(order_bp, url_prefix='/orders')
bp.register_blueprint(reward_bp, url_prefix='/rewards')
bp.register_blueprint(payment_bp, url_prefix='/payments')