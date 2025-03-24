from flask import Blueprint, jsonify
from app.services.payment_service import process_payment

bp = Blueprint('payment_routes', __name__)

@bp.route('/payment', methods=['POST'])
def payment():
    return process_payment()
