from flask import Blueprint

"""
Este módulo inicializa y registra los blueprints para las rutas de la aplicación Flask.

Los blueprints permiten organizar las rutas en módulos separados, facilitando
la escalabilidad y el mantenimiento del código.
"""

# Define blueprints for modular routes
bp = Blueprint("main", __name__)

# Import route modules to register them
from . import (
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