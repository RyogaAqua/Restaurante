from flask import Blueprint

# Create a blueprint for the routes package
bp = Blueprint('routes', __name__)

# Import and register individual blueprints
from app.routes.auth_routes import bp as auth_bp
from app.routes.menu_routes import bp as menu_bp
from app.routes.order_routes import bp as order_bp
from app.routes.reward_routes import bp as reward_bp
from app.routes.payment_routes import bp as payment_bp

# Register the blueprints with the main blueprint
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(menu_bp, url_prefix='/menu')
bp.register_blueprint(order_bp, url_prefix='/orders')
bp.register_blueprint(reward_bp, url_prefix='/rewards')
bp.register_blueprint(payment_bp, url_prefix='/payments')