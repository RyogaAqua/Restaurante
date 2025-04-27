from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService  # Cambiar a import relativo

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

@bp.route('/update-profile', methods=['PUT'])
def update_profile():
    """
    Ruta para actualizar el perfil del usuario.

    Procesa una solicitud PUT con los datos actualizados del usuario y actualiza
    la información en la base de datos.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()
        user_id = data.get('user_id')
        updated_data = {
            "nombre_usuario": data.get('nombre_usuario'),
            "apellido_usuario": data.get('apellido_usuario'),
            "email": data.get('email'),
            "telefono": data.get('telefono'),
            "address": data.get('address'),
        }

        # Llamar al método update_user_profile del servicio de autenticación
        updated_user = auth_service.update_user_profile(user_id, updated_data)
        return jsonify({"message": "Perfil actualizado exitosamente", "user": updated_user}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/change-password', methods=['PUT'])
def change_password():
    """
    Ruta para cambiar la contraseña del usuario.

    Procesa una solicitud PUT con la contraseña actual y la nueva contraseña,
    valida las credenciales y actualiza la contraseña en la base de datos.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        # Parsear los datos JSON de la solicitud
        data = request.get_json()
        user_id = data.get('user_id')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not user_id or not current_password or not new_password:
            raise ValueError("Faltan campos requeridos: user_id, current_password o new_password.")

        # Llamar al método change_user_password del servicio de autenticación
        auth_service.change_user_password(user_id, current_password, new_password)
        return jsonify({"message": "Contraseña actualizada exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Ruta para solicitar el restablecimiento de contraseña.

    Procesa una solicitud POST con el correo electrónico del usuario y envía un enlace
    de restablecimiento de contraseña al correo proporcionado.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            raise ValueError("El campo 'email' es obligatorio.")

        # Llamar al método send_password_reset_email del servicio de autenticación
        auth_service.send_password_reset_email(email)
        return jsonify({"message": "Correo de restablecimiento enviado exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Ruta para restablecer la contraseña del usuario.

    Procesa una solicitud POST con el token de restablecimiento y la nueva contraseña,
    valida el token y actualiza la contraseña en la base de datos.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito o error.
    """
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')

        if not token or not new_password:
            raise ValueError("Faltan campos requeridos: token o new_password.")

        # Llamar al método reset_password del servicio de autenticación
        auth_service.reset_password(token, new_password)
        return jsonify({"message": "Contraseña restablecida exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado", "details": str(e)}), 500