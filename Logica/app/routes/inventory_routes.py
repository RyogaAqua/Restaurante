from flask import Blueprint, request, jsonify
from ..services.inventory_service import InventoryService  # Import relativo

"""
Este módulo define las rutas relacionadas con el inventario, permitiendo
actualizar el stock de los elementos del menú y verificar su disponibilidad.
"""

# Crear un blueprint para las rutas de inventario
bp = Blueprint('inventory_routes', __name__)
inventory_service = InventoryService()  # Instanciar el servicio de inventario

@bp.route('/inventory/update', methods=['PUT'])
def update_stock():
    """
    Ruta para actualizar el stock de un elemento del menú.

    Procesa una solicitud PUT con el ID del elemento y la cantidad a actualizar.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        if not item_id or quantity is None:
            raise ValueError("Faltan campos requeridos: item_id o quantity.")

        inventory_service.update_stock(item_id, quantity)
        return jsonify({"message": "Stock actualizado exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/inventory/check', methods=['POST'])
def check_availability():
    """
    Ruta para verificar la disponibilidad de los elementos del menú.

    Procesa una solicitud POST con una lista de elementos y sus cantidades.

    Returns:
        Response: Respuesta JSON indicando si los elementos están disponibles o no.
    """
    try:
        data = request.get_json()
        items = data.get('items')

        if not items:
            raise ValueError("El campo 'items' es obligatorio.")

        availability = inventory_service.check_availability(items)
        return jsonify({"availability": availability}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500
