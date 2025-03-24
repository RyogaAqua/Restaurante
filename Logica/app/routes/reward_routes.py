from flask import Blueprint, jsonify
from app.services.reward_service import get_rewards

bp = Blueprint('reward_routes', __name__)

@bp.route('/rewards', methods=['GET'])
def rewards():
    return get_rewards()
