from flask import Blueprint, jsonify
from app.services.menu_service import get_menu

bp = Blueprint('menu_routes', __name__)

@bp.route('/menu', methods=['GET'])
def menu():
    return get_menu()
