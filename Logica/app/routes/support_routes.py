from flask import Blueprint, request, jsonify
from ..services.support_service import SupportService  # Import relativo

"""
Este módulo define las rutas relacionadas con el soporte, permitiendo a los usuarios
enviar mensajes al equipo de soporte y consultar el historial de interacciones.
"""

# Crear un blueprint para las rutas de soporte
bp = Blueprint('support_routes', __name__)
support_service = SupportService()  # Instanciar el servicio de soporte

@bp.route('/support/messages', methods=['POST'])
def send_message():
    """
    Ruta para enviar un mensaje al equipo de soporte.

    Procesa una solicitud POST con los datos del mensaje.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        subject = data.get('subject')
        message = data.get('message')

        if not user_id or not subject or not message:
            raise ValueError("Faltan campos requeridos: user_id, subject o message.")

        support_service.send_message(user_id, subject, message)
        return jsonify({"message": "Mensaje enviado exitosamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/support/messages', methods=['GET'])
def get_messages():
    """
    Ruta para obtener el historial de mensajes de un usuario.

    Procesa una solicitud GET con el parámetro `user_id`.

    Returns:
        Response: Respuesta JSON con los mensajes o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        messages = support_service.get_messages(user_id)
        return jsonify({"messages": messages}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
