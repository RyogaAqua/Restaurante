from flask import Blueprint, jsonify
from ..services.menu_service import get_menu

"""
Este módulo define las rutas relacionadas con el menú, permitiendo a los usuarios
recuperar los elementos disponibles en el menú.
"""

# Crear un blueprint para las rutas del menú
bp = Blueprint('menu_routes', __name__)

@bp.route('/menu', methods=['GET'])
def menu():
    """
    Ruta para obtener todos los elementos del menú.

    Procesa una solicitud GET y devuelve una lista de elementos del menú
    en formato JSON.

    Returns:
        Response: Respuesta JSON con los elementos del menú o un mensaje de error.
    """
    try:
        # Llamar a la función del servicio para obtener el menú
        menu_items = get_menu()
        return jsonify({"menu": menu_items}), 200
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500