import logging
from ..models import Orden, Usuario  # Corrected import to use the correct class name and relative import
from app.extensions import db  # Import db from extensions.py

class PaymentService:

    def __init__(self):
        # Use an environment variable for the payment gateway URL
        self.payment_gateway_url = "https://api.paymentgateway.com"  # Replace with a real URL or environment variable

    # Process a payment
    def process_payment(self, order_id, payment_method, payment_details):
        """
        Process the payment for an order.
        :param order_id: ID of the order.
        :param payment_method: Selected payment method (e.g., 'credit_card', 'paypal').
        :param payment_details: Payment details (e.g., card number, token).
        :return: Dictionary with the payment result.
        """
        try:
            # Retrieve the order
            order = Orden.query.get(order_id)
            if not order:
                raise ValueError("Order not found.")

            # Validate that the order is pending payment
            if order.estado != 'Pendiente':  # Updated to match the field name in the Orden model
                raise ValueError("This order is not in a pending state.")

            # Simulate payment processing (replace with real integration)
            payment_response = self._mock_payment_processing(payment_method, payment_details, order.precio_total)

            if payment_response.get('status') == 'success':
                # Update the order status to "Paid"
                order.estado = 'Pagado'  # Updated to match the field name in the Orden model
                db.session.commit()

                # Update user points after successful payment
                user = Usuario.query.get(order.id_usuario)  # Updated to use the correct class name and field name
                self.update_user_points(user, order.puntos)  # Updated to match the field name in the Orden model

                return {"message": "Payment processed successfully", "order_id": order_id, "status": "Paid"}
            else:
                raise ValueError("Payment was not successful. Please try again.")
        except Exception as e:
            logging.error(f"Error processing payment for order {order_id}: {e}")
            raise ValueError("An error occurred while processing the payment.")

    # Mock payment processing (replace with real integration)
    def _mock_payment_processing(self, payment_method, payment_details, amount):
        """
        Simulate payment processing. Replace this with real integration.
        :param payment_method: Payment method (e.g., 'credit_card', 'paypal').
        :param payment_details: Payment details (e.g., card number, token).
        :param amount: Amount to be paid.
        :return: Dictionary with the payment result.
        """
        # Simulate a successful payment response
        return {
            "status": "success",
            "transaction_id": "1234567890",  # Example transaction ID
            "amount": amount
        }

    # Update user points after a successful payment
    def update_user_points(self, user, points):
        """
        Update the user's points after a successful purchase.
        :param user: User whose points will be updated.
        :param points: Points to add or subtract.
        """
        try:
            user.puntos += points  # Updated to match the field name in the Usuario model
            db.session.commit()
        except Exception as e:
            logging.error(f"Error updating user points for user {user.id_usuario}: {e}")  # Updated field name
            raise ValueError("An error occurred while updating user points.")

    # Verify the status of a payment (replace with real payment gateway query)
    def verify_payment_status(self, transaction_id):
        """
        Verify the status of a payment by querying the payment gateway.
        :param transaction_id: Transaction ID from the payment gateway.
        :return: Dictionary with the payment status.
        """
        try:
            # Simulate querying the payment gateway
            payment_status = self._mock_payment_status(transaction_id)
            return payment_status
        except Exception as e:
            logging.error(f"Error verifying payment status for transaction {transaction_id}: {e}")
            raise ValueError("An error occurred while verifying the payment status.")

    # Mock payment status query (replace with real logic)
    def _mock_payment_status(self, transaction_id):
        """
        Simulate querying the payment status.
        :param transaction_id: Transaction ID to verify.
        :return: Dictionary with the payment status.
        """
        # Simulate a successful payment status response
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "payment_date": "2025-03-24"
        }