from ..models import MenuObjetos  # Import relativo
from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar el inventario, incluyendo la actualización
del stock y la verificación de disponibilidad de los elementos del menú.
"""

class InventoryService:
    """
    Servicio para manejar la lógica relacionada con el inventario.
    """

    def update_stock(self, item_id, quantity):
        """
        Actualiza el stock de un elemento del menú.

        Args:
            item_id (int): ID del elemento del menú.
            quantity (int): Cantidad a agregar o restar del stock.

        Raises:
            ValueError: Si el elemento no existe o ocurre un error al actualizar el stock.
        """
        try:
            item = MenuObjetos.query.get(item_id)
            if not item:
                raise ValueError("Elemento del menú no encontrado.")

            item.stock = (item.stock or 0) + quantity
            if item.stock < 0:
                raise ValueError("El stock no puede ser negativo.")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al actualizar el stock: {e}")

    def check_availability(self, items):
        """
        Verifica la disponibilidad de los elementos del menú.

        Args:
            items (list): Lista de diccionarios con 'item_id' y 'quantity'.

        Returns:
            list: Lista de elementos con su disponibilidad.
        """
        availability = []
        try:
            for item in items:
                menu_item = MenuObjetos.query.get(item['item_id'])
                if not menu_item:
                    availability.append({"item_id": item['item_id'], "available": False, "message": "Elemento no encontrado."})
                elif menu_item.stock is None or menu_item.stock < item['quantity']:
                    availability.append({"item_id": item['item_id'], "available": False, "message": "Stock insuficiente."})
                else:
                    availability.append({"item_id": item['item_id'], "available": True})

            return availability
        except Exception as e:
            raise ValueError(f"Error al verificar la disponibilidad: {e}")
