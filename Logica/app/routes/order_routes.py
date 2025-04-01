from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

bp = Blueprint('order_routes', __name__)
order_service = OrderService()  # Instantiate the OrderService class

@bp.route('/order', methods=['POST'])
def order():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Extract required fields from the request data
        user_id = data.get('user_id')
        restaurant_id = data.get('restaurant_id')
        items = data.get('items')
        address = data.get('address')

        # Validate required fields
        if not user_id or not restaurant_id or not items or not address:
            raise ValueError("Missing required fields: user_id, restaurant_id, items, or address.")

        # Call the create_order method of the OrderService class
        order_details = order_service.create_order(user_id, restaurant_id, items, address)

        # Return a success response
        return jsonify({"message": "Order created successfully", "order": order_details}), 201
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500