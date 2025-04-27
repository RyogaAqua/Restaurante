from flask import Blueprint, request, jsonify
from ..services.order_service import OrderService  # Cambiar a import relativo

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

@bp.route('/order/history', methods=['GET'])
def order_history():
    """
    Ruta para obtener el historial de pedidos de un usuario.

    Procesa una solicitud GET con el parámetro `user_id` para identificar al usuario
    y devuelve una lista de pedidos anteriores.

    Returns:
        Response: Respuesta JSON con el historial de pedidos o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id")

        # Llamar al método get_order_history del servicio de pedidos
        order_history = order_service.get_order_history(user_id)
        return jsonify({"orders": order_history}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500