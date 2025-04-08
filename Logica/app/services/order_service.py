import logging
from ..models import Orden, Restaurante, MenuObjetos, Usuario  # Importación correcta de las clases
from app.extensions import db  # Importa db desde extensions.py
from app.services.reward_service import RewardService

"""
Este módulo contiene la lógica para manejar pedidos, incluyendo la creación, validación,
cancelación, procesamiento de pagos y recuperación de pedidos.
"""

class OrderService:
    """
    Servicio para manejar la lógica relacionada con los pedidos.
    """

    def __init__(self):
        """
        Inicializa el servicio de pedidos y configura el servicio de recompensas.
        """
        self.reward_service = RewardService()

    def create_order(self, user_id, restaurant_id, items, address):
        """
        Crea un nuevo pedido en la base de datos.

        Args:
            user_id (int): ID del usuario que realiza el pedido.
            restaurant_id (int): ID del restaurante donde se realiza el pedido.
            items (list): Lista de elementos del menú incluidos en el pedido.
            address (str): Dirección de entrega del pedido.

        Returns:
            dict: Detalles del pedido creado, incluyendo precio total, puntos y calorías.

        Raises:
            ValueError: Si ocurre un error durante la creación del pedido.
        """
        try:
            # Validar usuario y restaurante
            user = self.get_user(user_id)
            restaurant = self.get_restaurant(restaurant_id)

            # Validar elementos del menú y calcular totales
            menu_items, total_price, total_calories = self.validate_menu_items(items)

            # Calcular puntos a ganar
            total_points = self.calculate_points(total_price)

            # Crear el pedido
            new_order = Orden(
                id_usuario=user_id,
                id_restaurante=restaurant_id,
                puntos=total_points,
                precio_total=total_price,
                direccion=address,
                estado="Pending"
            )

            # Guardar el pedido en la base de datos
            db.session.add(new_order)
            db.session.commit()

            # Actualizar los puntos del usuario
            self.reward_service.update_user_points(user, total_points)

            return {
                "message": "Pedido creado exitosamente",
                "order_id": new_order.id_orden,
                "total_price": total_price,
                "total_points": total_points,
                "total_calories": total_calories
            }
        except Exception as e:
            logging.error(f"Error al crear el pedido: {e}")
            raise ValueError("Ocurrió un error al crear el pedido.")

    def validate_menu_items(self, items):
        """
        Valida los elementos del menú y calcula los totales.

        Args:
            items (list): Lista de elementos del menú.

        Returns:
            tuple: Lista de objetos del menú, precio total y calorías totales.

        Raises:
            ValueError: Si algún elemento del menú no existe.
        """
        menu_items = []
        total_price = 0
        total_calories = 0

        for item in items:
            menu_item = MenuObjetos.query.filter_by(upc_objeto=item['UPC']).first()
            if not menu_item:
                raise ValueError(f"El elemento del menú con UPC {item['UPC']} no existe.")
            
            menu_items.append(menu_item)
            total_price += menu_item.precio
            total_calories += menu_item.calorias

        return menu_items, total_price, total_calories

    def calculate_points(self, total_price):
        """
        Calcula los puntos basados en el precio total.

        Args:
            total_price (float): Precio total del pedido.

        Returns:
            int: Puntos calculados.
        """
        return total_price // 10  # Ejemplo: 1 punto por cada 10 unidades de precio

    def get_orders_for_user(self, user_id):
        """
        Recupera los pedidos realizados por un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de pedidos realizados por el usuario.

        Raises:
            ValueError: Si ocurre un error al recuperar los pedidos.
        """
        try:
            orders = Orden.query.filter_by(id_usuario=user_id).all()
            if not orders:
                return {"message": "No se encontraron pedidos para este usuario."}

            orders_data = []
            for order in orders:
                restaurant = self.get_restaurant(order.id_restaurante)
                order_data = {
                    "order_id": order.id_orden,
                    "restaurant_name": restaurant.nombre,
                    "total_price": order.precio_total,
                    "total_points": order.puntos,
                    "address": order.direccion,
                    "order_status": order.estado,
                }
                orders_data.append(order_data)

            return orders_data
        except Exception as e:
            logging.error(f"Error al recuperar los pedidos para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al recuperar los pedidos.")

    def cancel_order(self, order_id):
        """
        Cancela un pedido existente.

        Args:
            order_id (int): ID del pedido a cancelar.

        Returns:
            dict: Mensaje de éxito indicando que el pedido fue cancelado.

        Raises:
            ValueError: Si ocurre un error al cancelar el pedido.
        """
        try:
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Pedido no encontrado.")

            # Actualizar el estado del pedido
            order.estado = 'Cancelled'

            # Revertir los puntos del usuario
            user = self.get_user(order.id_usuario)
            self.reward_service.update_user_points(user, -order.puntos)

            db.session.commit()

            return {"message": "Pedido cancelado exitosamente"}
        except Exception as e:
            logging.error(f"Error al cancelar el pedido {order_id}: {e}")
            raise ValueError("Ocurrió un error al cancelar el pedido.")

    def process_payment(self, order_id, payment_method):
        """
        Procesa el pago de un pedido.

        Args:
            order_id (int): ID del pedido.
            payment_method (str): Método de pago utilizado.

        Returns:
            dict: Mensaje indicando el estado del pago.

        Raises:
            ValueError: Si ocurre un error al procesar el pago.
        """
        try:
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Pedido no encontrado.")

            # Simular el procesamiento del pago
            payment_status = "Paid"

            # Actualizar el estado del pedido
            order.estado = payment_status
            db.session.commit()

            return {"message": f"Pago procesado exitosamente. Estado del pedido: {payment_status}"}
        except Exception as e:
            logging.error(f"Error al procesar el pago para el pedido {order_id}: {e}")
            raise ValueError("Ocurrió un error al procesar el pago.")

    def get_user(self, user_id):
        """
        Recupera un usuario por su ID.

        Args:
            user_id (int): ID del usuario.

        Returns:
            Usuario: El objeto del usuario.

        Raises:
            ValueError: Si el usuario no existe.
        """
        user = Usuario.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")
        return user

    def get_restaurant(self, restaurant_id):
        """
        Recupera un restaurante por su ID.

        Args:
            restaurant_id (int): ID del restaurante.

        Returns:
            Restaurante: El objeto del restaurante.

        Raises:
            ValueError: Si el restaurante no existe.
        """
        restaurant = Restaurante.query.get(restaurant_id)
        if not restaurant:
            raise ValueError("Restaurante no encontrado.")
        return restaurant