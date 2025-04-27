from flask import Blueprint, request, jsonify
from ..services.stats_service import StatsService  # Import relativo

"""
Este módulo define las rutas relacionadas con las estadísticas, permitiendo a los usuarios
consultar estadísticas personales y generales.
"""

# Crear un blueprint para las rutas de estadísticas
bp = Blueprint('stats_routes', __name__)
stats_service = StatsService()  # Instanciar el servicio de estadísticas

@bp.route('/stats/user', methods=['GET'])
def user_stats():
    """
    Ruta para obtener estadísticas personales de un usuario.

    Procesa una solicitud GET con el parámetro `user_id`.

    Returns:
        Response: Respuesta JSON con las estadísticas del usuario o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        stats = stats_service.get_user_stats(user_id)
        return jsonify({"stats": stats}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
