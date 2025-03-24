from flask import Blueprint, jsonify
from app.services.order_service import create_order

bp = Blueprint('order_routes', __name__)

@bp.route('/order', methods=['POST'])
def order():
    return create_order()
