from flask import Blueprint, request, jsonify
from app.services.reward_service import RewardService

"""
Este módulo define las rutas relacionadas con las recompensas, permitiendo a los usuarios
consultar las recompensas disponibles basadas en sus puntos.
"""

# Crear un blueprint para las rutas de recompensas
bp = Blueprint('reward_routes', __name__)
reward_service = RewardService()  # Instanciar la clase RewardService

@bp.route('/rewards', methods=['GET'])
def rewards():
    """
    Ruta para obtener las recompensas disponibles para un usuario.

    Procesa una solicitud GET con el parámetro `user_id` para identificar al usuario
    y devuelve una lista de recompensas disponibles basadas en los puntos del usuario.

    Returns:
        Response: Respuesta JSON con las recompensas disponibles o un mensaje de error.
    """
    try:
        # Extraer el parámetro user_id de los parámetros de consulta
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id")

        # Llamar al método get_available_rewards de la clase RewardService
        rewards_list = reward_service.get_available_rewards(user_id)

        # Devolver una respuesta de éxito
        return jsonify({"rewards": rewards_list}), 200
    except ValueError as e:
        # Manejar errores de validación
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Manejar errores inesperados
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500