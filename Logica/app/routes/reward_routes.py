from flask import Blueprint, request, jsonify
from app.services.reward_service import RewardService

bp = Blueprint('reward_routes', __name__)
reward_service = RewardService()  # Instantiate the RewardService class

@bp.route('/rewards', methods=['GET'])
def rewards():
    try:
        # Extract user_id from query parameters
        user_id = request.args.get('user_id')
        if not user_id:
            raise ValueError("Missing required parameter: user_id")

        # Call the get_available_rewards method of the RewardService class
        rewards_list = reward_service.get_available_rewards(user_id)

        # Return a success response
        return jsonify({"rewards": rewards_list}), 200
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500