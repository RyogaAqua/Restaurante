from flask import Blueprint, request, jsonify
from app.services.payment_service import PaymentService

bp = Blueprint('payment_routes', __name__)
payment_service = PaymentService()  # Instantiate the PaymentService class

@bp.route('/payment', methods=['POST'])
def payment():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Extract required fields from the request data
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        payment_details = data.get('payment_details')

        # Validate required fields
        if not order_id or not payment_method or not payment_details:
            raise ValueError("Missing required fields: order_id, payment_method, or payment_details.")

        # Call the process_payment method of the PaymentService class
        payment_result = payment_service.process_payment(order_id, payment_method, payment_details)

        # Return a success response
        return jsonify({"message": "Payment processed successfully", "details": payment_result}), 200
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500