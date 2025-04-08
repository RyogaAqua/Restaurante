from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

"""
Este módulo define las rutas relacionadas con los pedidos, permitiendo a los usuarios
crear nuevos pedidos y manejar la lógica asociada.
"""

# Crear un blueprint para las rutas de pedidos
bp = Blueprint('order_routes', __name__)
order_service = OrderService()  # Instanciar la clase OrderService

@bp.route('/order', methods=['POST'])
def order():
    """
    Ruta para crear un nuevo pedido.

    Procesa una solicitud POST con los datos del pedido, como el ID del usuario,
    el ID del restaurante, los elementos del menú y la dirección de entrega.

    Returns:
        Response: Respuesta JSON con los detalles del pedido creado o un mensaje de error.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()

        # Extraer los campos requeridos de los datos de la solicitud
        user_id = data.get('user_id')
        restaurant_id = data.get('restaurant_id')
        items = data.get('items')
        address = data.get('address')

        # Validar los campos requeridos
        if not user_id or not restaurant_id or not items or not address:
            raise ValueError("Faltan campos requeridos: user_id, restaurant_id, items o address.")

        # Llamar al método create_order de la clase OrderService
        order_details = order_service.create_order(user_id, restaurant_id, items, address)

        # Devolver una respuesta de éxito
        return jsonify({"message": "Pedido creado exitosamente", "order": order_details}), 201
    except ValueError as e:
        # Manejar errores de validación
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Manejar errores inesperados
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500