from flask import Blueprint

"""
Este módulo inicializa y registra los blueprints para las rutas de la aplicación Flask.

Los blueprints permiten organizar las rutas en módulos separados, facilitando
la escalabilidad y el mantenimiento del código.
"""

# Crear un blueprint para el paquete de rutas
bp = Blueprint('routes', __name__)

# Importar y registrar blueprints individuales
from app.routes.auth_routes import bp as auth_bp  # Rutas relacionadas con autenticación
from app.routes.menu_routes import bp as menu_bp  # Rutas relacionadas con el menú
from app.routes.order_routes import bp as order_bp  # Rutas relacionadas con pedidos
from app.routes.reward_routes import bp as reward_bp  # Rutas relacionadas con recompensas
from app.routes.payment_routes import bp as payment_bp  # Rutas relacionadas con pagos

# Registrar los blueprints con el blueprint principal
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(menu_bp, url_prefix='/menu')
bp.register_blueprint(order_bp, url_prefix='/orders')
bp.register_blueprint(reward_bp, url_prefix='/rewards')
bp.register_blueprint(payment_bp, url_prefix='/payments')