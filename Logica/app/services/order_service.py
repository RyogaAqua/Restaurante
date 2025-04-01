import logging
from ..models import Orden, Restaurante, MenuObjetos, Usuario  # Updated to use the correct class name
from app.extensions import db  # Import db from extensions.py
from app.services.reward_service import RewardService

class OrderService:

    def __init__(self):
        self.reward_service = RewardService()

    # Create a new order
    def create_order(self, user_id, restaurant_id, items, address):
        try:
            # Validate user and restaurant
            user = self.get_user(user_id)
            restaurant = self.get_restaurant(restaurant_id)

            # Validate menu items and calculate totals
            menu_items, total_price, total_calories = self.validate_menu_items(items)

            # Calculate points to be earned
            total_points = self.calculate_points(total_price)

            # Create the order
            new_order = Orden(
                id_usuario=user_id,
                id_restaurante=restaurant_id,
                puntos=total_points,
                precio_total=total_price,
                direccion=address,
                estado="Pending"
            )

            # Save the order to the database
            db.session.add(new_order)
            db.session.commit()

            # Update user points
            self.reward_service.update_user_points(user, total_points)

            return {
                "message": "Order created successfully",
                "order_id": new_order.id_orden,
                "total_price": total_price,
                "total_points": total_points,
                "total_calories": total_calories
            }
        except Exception as e:
            logging.error(f"Error creating order: {e}")
            raise ValueError("An error occurred while creating the order.")

    # Validate menu items and calculate totals
    def validate_menu_items(self, items):
        menu_items = []
        total_price = 0
        total_calories = 0

        for item in items:
            menu_item = MenuObjetos.query.filter_by(upc_objeto=item['UPC']).first()
            if not menu_item:
                raise ValueError(f"Menu item with UPC {item['UPC']} does not exist.")
            
            menu_items.append(menu_item)
            total_price += menu_item.precio
            total_calories += menu_item.calorias

        return menu_items, total_price, total_calories

    # Calculate points based on total price
    def calculate_points(self, total_price):
        # Example: 1 point for every 10 units of price
        return total_price // 10

    # Get orders for a user
    def get_orders_for_user(self, user_id):
        try:
            orders = Orden.query.filter_by(id_usuario=user_id).all()
            if not orders:
                return {"message": "No orders found for this user."}

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
            logging.error(f"Error retrieving orders for user {user_id}: {e}")
            raise ValueError("An error occurred while retrieving orders.")

    # Cancel an order
    def cancel_order(self, order_id):
        try:
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Order not found.")

            # Update order status
            order.estado = 'Cancelled'

            # Revert user points
            user = self.get_user(order.id_usuario)
            self.reward_service.update_user_points(user, -order.puntos)

            db.session.commit()

            return {"message": "Order cancelled successfully"}
        except Exception as e:
            logging.error(f"Error cancelling order {order_id}: {e}")
            raise ValueError("An error occurred while cancelling the order.")

    # Process a payment
    def process_payment(self, order_id, payment_method):
        try:
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Order not found.")

            # Simulate payment processing
            payment_status = "Paid"

            # Update order status
            order.estado = payment_status
            db.session.commit()

            return {"message": f"Payment processed successfully. Order status: {payment_status}"}
        except Exception as e:
            logging.error(f"Error processing payment for order {order_id}: {e}")
            raise ValueError("An error occurred while processing the payment.")

    # Helper method to get a user
    def get_user(self, user_id):
        user = Usuario.query.get(user_id)  # Updated to use the correct class name
        if not user:
            raise ValueError("User not found.")
        return user

    # Helper method to get a restaurant
    def get_restaurant(self, restaurant_id):
        restaurant = Restaurante.query.get(restaurant_id)
        if not restaurant:
            raise ValueError("Restaurant not found.")
        return restaurant