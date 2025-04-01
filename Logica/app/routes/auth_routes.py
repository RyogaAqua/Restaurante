from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

bp = Blueprint('auth_routes', __name__)
auth_service = AuthService()  # Instantiate the AuthService

@bp.route('/login', methods=['POST'])
def login():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Call the login_user method from AuthService
        token = auth_service.login_user(email, password)
        return jsonify({"message": "Login successful", "token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@bp.route('/register', methods=['POST'])
def register():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        nombre_usuario = data.get('nombre_usuario')
        apellido_usuario = data.get('apellido_usuario')
        email = data.get('email')
        telefono = data.get('telefono')
        contrasena = data.get('contrasena')
        address = data.get('address')
        metodo_pago = data.get('metodo_pago')

        # Call the register_user method from AuthService
        auth_service.register_user(
            nombre_usuario, apellido_usuario, email, telefono, contrasena, address, metodo_pago
        )
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500