from ..models import MenuObjetos  # Ensure only valid models are imported
from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar el carrito, incluyendo guardar y recuperar
los datos del carrito desde la base de datos.
"""

class CartService:
    """
    Servicio para manejar la lógica relacionada con el carrito.
    """

    def save_cart(self, user_id, cart_items):
        """
        Guarda el carrito del usuario en la base de datos.

        Args:
            user_id (int): ID del usuario.
            cart_items (list): Lista de elementos del carrito.

        Raises:
            ValueError: Si ocurre un error al guardar el carrito.
        """
        try:
            # Eliminar los elementos existentes del carrito del usuario
            CartItem.query.filter_by(user_id=user_id).delete()

            # Agregar los nuevos elementos del carrito
            for item in cart_items:
                menu_item = MenuObjetos.query.get(item['id_objeto'])
                if not menu_item:
                    raise ValueError(f"El elemento del menú con ID {item['id_objeto']} no existe.")

                cart_item = CartItem(
                    user_id=user_id,
                    id_objeto=item['id_objeto'],
                    quantity=item['quantity']
                )
                db.session.add(cart_item)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al guardar el carrito: {e}")

    def get_cart(self, user_id):
        """
        Recupera el carrito del usuario desde la base de datos.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de elementos del carrito.

        Raises:
            ValueError: Si ocurre un error al recuperar el carrito.
        """
        try:
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            return [
                {
                    "id_objeto": item.id_objeto,
                    "nombre_objeto": item.menu_objeto.nombre_objeto,
                    "quantity": item.quantity,
                    "precio": float(item.menu_objeto.precio)
                }
                for item in cart_items
            ]
        except Exception as e:
            raise ValueError(f"Error al recuperar el carrito: {e}")
