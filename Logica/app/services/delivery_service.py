from ..models import Orden  # Import relativo
from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar las entregas, incluyendo el seguimiento
del estado de los pedidos.
"""

class DeliveryService:
    """
    Servicio para manejar la lógica relacionada con las entregas.
    """

    def get_delivery_status(self, order_id):
        """
        Recupera el estado de entrega de un pedido.

        Args:
            order_id (int): ID del pedido.

        Returns:
            str: Estado actual del pedido.

        Raises:
            ValueError: Si el pedido no existe o ocurre un error.
        """
        try:
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Pedido no encontrado.")

            # Simular estados de entrega (esto debería estar en la base de datos)
            delivery_status = {
                1: "Preparando",
                2: "En camino",
                3: "Entregado"
            }

            # Determinar el estado basado en un campo ficticio `estado_entrega`
            estado_entrega = getattr(order, 'estado_entrega', 1)  # Por defecto, "Preparando"
            return delivery_status.get(estado_entrega, "Desconocido")
        except Exception as e:
            raise ValueError(f"Error al recuperar el estado de entrega: {e}")
