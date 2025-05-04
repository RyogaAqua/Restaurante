import logging
from ..models import Orden, OrdenItems, Usuarios, PuntosBalance  # Modelos basados en RestauranteWKDB.sql
from ..extensions import db  # Import relativo correcto

"""
Este módulo contiene la lógica para manejar los pagos, incluyendo el procesamiento,
la verificación del estado de los pagos y la actualización de puntos de usuario.
"""

class PaymentService:
    """
    Servicio para manejar la lógica relacionada con los pagos.
    """

    def __init__(self):
        """
        Inicializa el servicio de pagos y configura la URL del gateway de pagos.
        """
        # Usar una variable de entorno para la URL del gateway de pagos
        self.payment_gateway_url = "https://api.paymentgateway.com"  # Reemplazar con una URL real o variable de entorno

    def process_payment(self, order_id, payment_method, payment_details):
        """
        Procesa el pago de un pedido.

        Args:
            order_id (int): ID del pedido.
            payment_method (str): Método de pago seleccionado (por ejemplo, 'credit_card', 'paypal').
            payment_details (dict): Detalles del pago (por ejemplo, número de tarjeta, token).

        Returns:
            dict: Resultado del pago, incluyendo el estado y el ID del pedido.

        Raises:
            ValueError: Si ocurre un error durante el procesamiento del pago.
        """
        try:
            # Recuperar el pedido
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Pedido no encontrado.")

            # Validar que el pedido esté pendiente de pago
            if order.estado != 'Pendiente':  # Validar el estado del pedido
                raise ValueError("Este pedido no está en estado pendiente.")

            # Simular el procesamiento del pago (reemplazar con integración real)
            payment_response = self._mock_payment_processing(payment_method, payment_details, order.precio_total)

            if payment_response.get('status') == 'success':
                # Actualizar el estado del pedido a "Pagado"
                order.estado = 'Pagado'
                db.session.commit()

                # Actualizar los puntos del usuario después del pago exitoso
                self.update_user_points(order.id_usuario, order.puntos_ganados)

                return {"message": "Pago procesado exitosamente", "order_id": order_id, "status": "Paid"}
            else:
                raise ValueError("El pago no fue exitoso. Por favor, inténtelo de nuevo.")
        except Exception as e:
            logging.error(f"Error al procesar el pago para el pedido {order_id}: {e}")
            raise ValueError("Ocurrió un error al procesar el pago.")

    def _mock_payment_processing(self, payment_method, payment_details, amount):
        """
        Simula el procesamiento del pago. Reemplazar con integración real.

        Args:
            payment_method (str): Método de pago (por ejemplo, 'credit_card', 'paypal').
            payment_details (dict): Detalles del pago (por ejemplo, número de tarjeta, token).
            amount (float): Monto a pagar.

        Returns:
            dict: Resultado simulado del pago.
        """
        # Simular una respuesta de pago exitoso
        return {
            "status": "success",
            "transaction_id": "1234567890",  # Ejemplo de ID de transacción
            "amount": amount
        }

    def update_user_points(self, user_id, points_earned):
        """
        Actualiza los puntos del usuario después de una compra exitosa.

        Args:
            user_id (int): ID del usuario cuyos puntos serán actualizados.
            points_earned (int): Puntos ganados en la transacción.

        Raises:
            ValueError: Si ocurre un error al actualizar los puntos del usuario.
        """
        try:
            puntos_balance = PuntosBalance.query.get(user_id)
            if not puntos_balance:
                raise ValueError("Usuario no encontrado o sin balance de puntos.")

            puntos_balance.puntos_total += points_earned
            db.session.commit()
        except Exception as e:
            logging.error(f"Error al actualizar los puntos del usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al actualizar los puntos del usuario.")

    def verify_payment_status(self, transaction_id):
        """
        Verifica el estado de un pago consultando el gateway de pagos.

        Args:
            transaction_id (str): ID de la transacción del gateway de pagos.

        Returns:
            dict: Estado del pago.

        Raises:
            ValueError: Si ocurre un error al verificar el estado del pago.
        """
        try:
            # Simular la consulta al gateway de pagos
            payment_status = self._mock_payment_status(transaction_id)
            return payment_status
        except Exception as e:
            logging.error(f"Error al verificar el estado del pago para la transacción {transaction_id}: {e}")
            raise ValueError("Ocurrió un error al verificar el estado del pago.")

    def _mock_payment_status(self, transaction_id):
        """
        Simula la consulta del estado del pago.

        Args:
            transaction_id (str): ID de la transacción a verificar.

        Returns:
            dict: Estado simulado del pago.
        """
        # Simular una respuesta de estado de pago exitoso
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "payment_date": "2025-03-24"
        }

    def get_payment_history(self, user_id):
        """
        Recupera el historial de pagos de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de pagos realizados por el usuario.

        Raises:
            ValueError: Si ocurre un error al recuperar el historial de pagos.
        """
        try:
            # Recuperar los pedidos pagados del usuario
            orders = Orden.query.filter_by(id_usuario=user_id, estado='Pagado').all()
            payment_history = []

            for order in orders:
                payment_history.append({
                    "order_id": order.id_orden,
                    "total_price": float(order.precio_total),
                    "payment_date": order.fecha_orden.strftime('%Y-%m-%d %H:%M:%S'),
                    "points_earned": order.puntos_ganados,
                    "points_spent": order.puntos_gastados
                })

            return payment_history
        except Exception as e:
            logging.error(f"Error al recuperar el historial de pagos para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al recuperar el historial de pagos.")