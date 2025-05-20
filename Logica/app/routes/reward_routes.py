from flask import Blueprint, request, jsonify
from ..services.reward_service import RewardService  # Cambiar a import relativo

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

@bp.route('/rewards/redeem', methods=['POST'])
def redeem():
    """
    Ruta para canjear una recompensa.

    Procesa una solicitud POST con el ID del usuario y el nombre de la recompensa.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        reward_name = data.get('reward_name')

        if not user_id or not reward_name:
            raise ValueError("Faltan campos requeridos: user_id o reward_name.")

        result = reward_service.redeem_reward(user_id, reward_name)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500