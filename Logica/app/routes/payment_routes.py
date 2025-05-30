from flask import Blueprint, request, jsonify
from ..services.payment_service import PaymentService  # Cambiar a import relativo

"""
Este módulo define las rutas relacionadas con los pagos, permitiendo a los usuarios
procesar pagos para pedidos y manejar la lógica asociada.
"""

# Crear un blueprint para las rutas de pagos
bp = Blueprint('payment_routes', __name__)
payment_service = PaymentService()  # Instanciar la clase PaymentService

@bp.route('/payment', methods=['POST'])
def payment():
    """
    Ruta para procesar un pago.

    Procesa una solicitud POST con los datos del pago, como el ID del pedido,
    el método de pago y los detalles del pago.

    Returns:
        Response: Respuesta JSON con los detalles del resultado del pago o un mensaje de error.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()

        # Extraer los campos requeridos de los datos de la solicitud
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        payment_details = data.get('payment_details')

        # Validar los campos requeridos
        if not order_id or not payment_method or not payment_details:
            raise ValueError("Faltan campos requeridos: order_id, payment_method o payment_details.")

        # Llamar al método process_payment de la clase PaymentService
        payment_result = payment_service.process_payment(order_id, payment_method, payment_details)

        # Devolver una respuesta de éxito
        return jsonify({"message": "Pago procesado exitosamente", "details": payment_result}), 200
    except ValueError as e:
        # Manejar errores de validación
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Manejar errores inesperados
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/payment/history', methods=['GET'])
def payment_history():
    """
    Ruta para obtener el historial de pagos de un usuario.

    Procesa una solicitud GET con el parámetro `user_id` para identificar al usuario
    y devuelve una lista de pagos realizados.

    Returns:
        Response: Respuesta JSON con el historial de pagos o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        # Llamar al método get_payment_history del servicio de pagos
        payment_history = payment_service.get_payment_history(user_id)
        return jsonify({"payments": payment_history}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500