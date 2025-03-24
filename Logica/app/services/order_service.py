from app.models import Orden, Restaurante, Menu_Objetos, Usuarios, Puntos
from app.config import db
from app.services.reward_service import RewardService

class OrderService:

    def __init__(self):
        self.reward_service = RewardService()

    # Método para crear un nuevo pedido
    def create_order(self, user_id, restaurant_id, items, address):
        # Obtener el restaurante y el usuario
        user = Usuarios.query.get(user_id)
        restaurant = Restaurante.query.get(restaurant_id)

        if not user or not restaurant:
            raise ValueError("Usuario o restaurante no encontrado.")

        # Verificar que los elementos del menú existen
        menu_items = []
        total_price = 0
        total_calories = 0

        for item in items:
            menu_item = Menu_Objetos.query.filter_by(UPC_Objeto=item['UPC']).first()
            if not menu_item:
                raise ValueError(f"El elemento con UPC {item['UPC']} no existe.")
            
            menu_items.append(menu_item)
            total_price += menu_item.Precio
            total_calories += menu_item.Calorias

        # Calcular los puntos a ganar por el pedido
        total_points = self.calculate_points(total_price)

        # Crear el pedido
        new_order = Orden(
            Id_Usuario=user_id,
            Restaurante=restaurant_id,
            Puntos=total_points,
            Precio_Total=total_price,
            Puntos_Total=total_points,
            Address=address
        )

        # Agregar el pedido a la base de datos
        db.session.add(new_order)
        db.session.commit()

        # Actualizar los puntos del usuario
        self.reward_service.update_user_points(user, total_points)

        return {
            "message": "Pedido creado con éxito",
            "order_id": new_order.Id_Transaccion,
            "total_price": total_price,
            "total_points": total_points,
            "total_calories": total_calories
        }

    # Método para calcular puntos basados en el precio del pedido
    def calculate_points(self, total_price):
        # Aquí puedes implementar la lógica para calcular los puntos.
        # Ejemplo: 1 punto por cada 10 unidades de precio.
        return total_price // 10  # Se pueden modificar las reglas de puntos según sea necesario.

    # Método para obtener las órdenes de un usuario
    def get_orders_for_user(self, user_id):
        orders = Orden.query.filter_by(Id_Usuario=user_id).all()
        if not orders:
            return {"message": "No hay pedidos para este usuario."}

        orders_data = []
        for order in orders:
            restaurant = Restaurante.query.get(order.Restaurante)
            order_data = {
                "order_id": order.Id_Transaccion,
                "restaurant_name": restaurant.Nombre,
                "total_price": order.Precio_Total,
                "total_points": order.Puntos_Total,
                "address": order.Address,
                "order_status": order.Estado if hasattr(order, 'Estado') else "Pendiente",
            }
            orders_data.append(order_data)

        return orders_data

    # Método para cancelar un pedido
    def cancel_order(self, order_id):
        order = Orden.query.get(order_id)
        if not order:
            raise ValueError("Pedido no encontrado.")

        # Actualizar el estado del pedido (si se desea manejar estados)
        order.Estado = 'Cancelado'

        # Revertir puntos si ya se han asignado
        user = Usuarios.query.get(order.Id_Usuario)
        self.reward_service.update_user_points(user, -order.Puntos_Total)

        db.session.commit()

        return {"message": "Pedido cancelado con éxito"}

    # Método para procesar un pago (se podría conectar con un servicio de pago real)
    def process_payment(self, order_id, payment_method):
        order = Orden.query.get(order_id)
        if not order:
            raise ValueError("Pedido no encontrado.")

        # Aquí deberías agregar la lógica para procesar el pago con el método de pago proporcionado
        # Esto podría involucrar una integración con un API de pago (por ejemplo, Stripe o PayPal)
        
        # Simulación de un pago exitoso
        payment_status = "Pagado"

        # Actualizar el estado del pedido
        order.Estado = payment_status
        db.session.commit()

        return {"message": f"Pago procesado exitosamente. Estado del pedido: {payment_status}"}
