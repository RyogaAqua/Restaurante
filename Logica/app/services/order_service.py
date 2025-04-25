import logging
from ..models import Orden, MenuObjetos, Usuario, Address, OrdenItems  # Cambiar a import relativo
from ..extensions import db  # Import relativo correcto
from ..services.reward_service import RewardService  # Cambiar a import relativo

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

    def create_order(self, user_id, restaurant_id, items, delivery_address):
        """
        Crea un nuevo pedido en la base de datos.

        Args:
            user_id (int): ID del usuario que realiza el pedido.
            restaurant_id (int): ID del restaurante donde se realiza el pedido.
            items (list): Lista de elementos del menú incluidos en el pedido.
            delivery_address (dict): Dirección de entrega del pedido.

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
            total_points_earned = self.calculate_points(total_price)

            # Crear o buscar la dirección de entrega
            address = self.get_or_create_address(delivery_address)

            # Crear el pedido
            new_order = Orden(
                id_usuario=user_id,
                id_delivery_address=address.id_address,
                precio_total=total_price,
                puntos_gastados=0,  # Inicialmente no se gastan puntos
                puntos_ganados=total_points_earned
            )
            db.session.add(new_order)
            db.session.flush()  # Asegura que el pedido tenga un ID antes de agregar los items

            # Agregar los items al pedido
            for item in menu_items:
                order_item = OrdenItems(
                    id_transaccion=new_order.id_transaccion,
                    id_objeto=item['id_objeto'],
                    quantity=item['quantity'],
                    precio_unitario_congelado=item['precio']
                )
                db.session.add(order_item)

            # Guardar el pedido y los items
            db.session.commit()

            # Actualizar los puntos del usuario
            self.reward_service.update_user_points(user_id, total_points_earned)

            return {
                "message": "Pedido creado exitosamente",
                "order_id": new_order.id_transaccion,
                "total_price": total_price,
                "total_points_earned": total_points_earned,
                "total_calories": total_calories
            }
        except Exception as e:
            db.session.rollback()
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
            menu_item = MenuObjetos.query.get(item['id_objeto'])
            if not menu_item:
                raise ValueError(f"El elemento del menú con ID {item['id_objeto']} no existe.")
            
            menu_items.append({
                "id_objeto": menu_item.id_objeto,
                "quantity": item['quantity'],
                "precio": menu_item.precio,
                "calorias": menu_item.calorias
            })
            total_price += menu_item.precio * item['quantity']
            total_calories += menu_item.calorias * item['quantity']

        return menu_items, total_price, total_calories

    def calculate_points(self, total_price):
        """
        Calcula los puntos basados en el precio total.

        Args:
            total_price (float): Precio total del pedido.

        Returns:
            int: Puntos calculados.
        """
        return int(total_price // 10)  # Ejemplo: 1 punto por cada 10 unidades de precio

    def get_or_create_address(self, address_data):
        """
        Crea o busca una dirección en la base de datos.

        Args:
            address_data (dict): Diccionario con los detalles de la dirección.

        Returns:
            Address: Objeto de la dirección.
        """
        address = Address.query.filter_by(
            address=address_data.get('address'),
            city=address_data.get('city'),
            state=address_data.get('state'),
            zip_code=address_data.get('zip_code'),
            country=address_data.get('country')
        ).first()

        if not address:
            address = Address(
                address=address_data.get('address'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                zip_code=address_data.get('zip_code'),
                country=address_data.get('country')
            )
            db.session.add(address)
            db.session.flush()  # Asegura que la dirección tenga un ID antes de usarla

        return address

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