from flask import Blueprint, request, jsonify
from ..services.notification_service import NotificationService  # Import relativo

"""
Este módulo define las rutas relacionadas con las notificaciones, permitiendo
enviar y recuperar notificaciones para los usuarios.
"""

# Crear un blueprint para las rutas de notificaciones
bp = Blueprint('notification_routes', __name__)
notification_service = NotificationService()  # Instanciar el servicio de notificaciones

@bp.route('/notifications', methods=['POST'])
def send_notification():
    """
    Ruta para enviar una notificación a un usuario.

    Procesa una solicitud POST con los datos de la notificación.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message = data.get('message')
        notification_type = data.get('type', 'info')  # Tipo de notificación (info, success, error)

        if not user_id or not message:
            raise ValueError("Faltan campos requeridos: user_id o message.")

        notification_service.send_notification(user_id, message, notification_type)
        return jsonify({"message": "Notificación enviada exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Ruta para obtener las notificaciones de un usuario.

    Procesa una solicitud GET con el parámetro `user_id`.

    Returns:
        Response: Respuesta JSON con las notificaciones o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        notifications = notification_service.get_notifications(user_id)
        return jsonify({"notifications": notifications}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
