from flask import Blueprint, request, jsonify
from ..services.delivery_service import DeliveryService  # Import relativo

"""
Este módulo define las rutas relacionadas con las entregas, permitiendo a los usuarios
rastrear el estado de sus pedidos.
"""

# Crear un blueprint para las rutas de entregas
bp = Blueprint('delivery_routes', __name__)
delivery_service = DeliveryService()  # Instanciar el servicio de entregas

@bp.route('/delivery/status', methods=['GET'])
def get_delivery_status():
    """
    Ruta para obtener el estado de entrega de un pedido.

    Procesa una solicitud GET con el parámetro `order_id`.

    Returns:
        Response: Respuesta JSON con el estado del pedido o un mensaje de error.
    """
    try:
        order_id = request.args.get('order_id')
        if not order_id:
            raise ValueError("Falta el parámetro requerido: order_id.")

        status = delivery_service.get_delivery_status(order_id)
        return jsonify({"order_id": order_id, "status": status}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
