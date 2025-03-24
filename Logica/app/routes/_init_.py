from flask import Blueprint

bp = Blueprint('routes', __name__)

from app.routes import auth_routes, menu_routes, order_routes, reward_routes, payment_routes
