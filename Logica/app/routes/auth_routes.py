from flask import Blueprint, request, jsonify
from app.services.auth_service import login_user, register_user

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['POST'])
def login():
    return login_user()

@bp.route('/register', methods=['POST'])
def register():
    return register_user()
