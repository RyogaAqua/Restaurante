from flask import Blueprint, jsonify
from app.services.menu_service import get_menu

bp = Blueprint('menu_routes', __name__)

@bp.route('/menu', methods=['GET'])
def menu():
    try:
        # Call the service function to get the menu
        menu_items = get_menu()
        return jsonify({"menu": menu_items}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500