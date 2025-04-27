from flask import Blueprint, request, jsonify
from ..services.cart_service import CartService  # Import relativo

"""
Este módulo define las rutas relacionadas con el carrito, permitiendo a los usuarios
guardar y recuperar su carrito desde el backend.
"""

# Crear un blueprint para las rutas del carrito
bp = Blueprint('cart_routes', __name__)
cart_service = CartService()  # Instanciar el servicio del carrito

@bp.route('/cart', methods=['POST'])
def save_cart():
    """
    Ruta para guardar el carrito del usuario en el backend.

    Procesa una solicitud POST con los datos del carrito y los guarda en la base de datos.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        cart_items = data.get('cart_items')

        if not user_id or not cart_items:
            raise ValueError("Faltan campos requeridos: user_id o cart_items.")

        cart_service.save_cart(user_id, cart_items)
        return jsonify({"message": "Carrito guardado exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/cart', methods=['GET'])
def get_cart():
    """
    Ruta para recuperar el carrito del usuario desde el backend.

    Procesa una solicitud GET con el parámetro `user_id` y devuelve los datos del carrito.

    Returns:
        Response: Respuesta JSON con los datos del carrito o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        cart_items = cart_service.get_cart(user_id)
        return jsonify({"cart_items": cart_items}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
