from flask import Blueprint, request, jsonify
from ..services.address_service import AddressService  # Import relativo

"""
Este módulo define las rutas relacionadas con las direcciones, permitiendo
a los usuarios agregar, eliminar y listar sus direcciones de entrega.
"""

# Crear un blueprint para las rutas de direcciones
bp = Blueprint('address_routes', __name__)
address_service = AddressService()  # Instanciar el servicio de direcciones

@bp.route('/addresses', methods=['POST'])
def add_address():
    """
    Ruta para agregar una nueva dirección para un usuario.

    Procesa una solicitud POST con los datos de la dirección.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        address_data = data.get('address')

        if not user_id or not address_data:
            raise ValueError("Faltan campos requeridos: user_id o address.")

        new_address = address_service.add_address(user_id, address_data)
        return jsonify({"message": "Dirección agregada exitosamente.", "address": new_address}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/addresses', methods=['GET'])
def list_addresses():
    """
    Ruta para listar todas las direcciones de un usuario.

    Procesa una solicitud GET con el parámetro `user_id`.

    Returns:
        Response: Respuesta JSON con las direcciones o un mensaje de error.
    """
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Falta el parámetro requerido: user_id.")

        addresses = address_service.list_addresses(user_id)
        return jsonify({"addresses": addresses}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """
    Ruta para eliminar una dirección de un usuario.

    Procesa una solicitud DELETE con el ID de la dirección.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        address_service.delete_address(address_id)
        return jsonify({"message": "Dirección eliminada exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
