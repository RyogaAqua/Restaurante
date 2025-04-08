from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

"""
Este módulo define las rutas relacionadas con la autenticación de usuarios,
incluyendo el inicio de sesión y el registro de nuevos usuarios.
"""

# Crear un blueprint para las rutas de autenticación
bp = Blueprint('auth_routes', __name__)
auth_service = AuthService()  # Instanciar el servicio de autenticación

@bp.route('/login', methods=['POST'])
def login():
    """
    Ruta para iniciar sesión.

    Procesa una solicitud POST con las credenciales del usuario (correo electrónico y contraseña),
    y devuelve un token de autenticación si las credenciales son válidas.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito y el token de autenticación,
                  o un mensaje de error en caso de fallo.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Llamar al método login_user del servicio de autenticación
        token = auth_service.login_user(email, password)
        return jsonify({"message": "Inicio de sesión exitoso", "token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500

@bp.route('/register', methods=['POST'])
def register():
    """
    Ruta para registrar un nuevo usuario.

    Procesa una solicitud POST con los datos del usuario (nombre, apellido, correo electrónico,
    teléfono, contraseña, dirección y método de pago) y registra al usuario en el sistema.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito si el registro es exitoso,
                  o un mensaje de error en caso de fallo.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()
        nombre_usuario = data.get('nombre_usuario')
        apellido_usuario = data.get('apellido_usuario')
        email = data.get('email')
        telefono = data.get('telefono')
        contrasena = data.get('contrasena')
        address = data.get('address')
        metodo_pago = data.get('metodo_pago')

        # Llamar al método register_user del servicio de autenticación
        auth_service.register_user(
            nombre_usuario, apellido_usuario, email, telefono, contrasena, address, metodo_pago
        )
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500