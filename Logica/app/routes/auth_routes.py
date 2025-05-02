from flask import Blueprint, request, jsonify, render_template
from ..services.auth_service import AuthService  # Cambiar a import relativo
from ..extensions import db
from Logica.app.models import Usuarios, Address, Puntos
from Logica.app.utils.security import hash_password  # Importar función para hashear contraseñas
import logging

"""
Este módulo define las rutas relacionadas con la autenticación de usuarios,
incluyendo el inicio de sesión y el registro de nuevos usuarios.
"""

# Crear un blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()  # Instanciar el servicio de autenticación

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        logging.info("Received registration request")
        data = request.get_json()
        logging.info(f"Request data: {data}")

        # Validar y procesar los datos enviados desde el frontend
        required_fields = ['nombre_usuario', 'apellido_usuario', 'email', 'telefono', 'contrasena', 'metodo_pago', 'address']
        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field: {field}")
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Validar dirección
        address_data = data['address']
        if not isinstance(address_data, dict):
            logging.error("Invalid address format")
            return jsonify({'error': 'Invalid address format'}), 400

        # Crear o verificar la dirección
        address = Address.query.filter_by(address=address_data['address']).first()
        if not address:
            address = Address(
                address=address_data['address'],
                zip_code=address_data.get('zip_code'),
                state=address_data.get('state'),
                country=address_data.get('country'),
                city=address_data.get('city')
            )
            db.session.add(address)
            db.session.flush()

        # Crear puntos iniciales
        puntos = Puntos(puntos_total=0)
        db.session.add(puntos)
        db.session.flush()

        # Crear usuario con contraseña hasheada
        hashed_password = hash_password(data['contrasena'])
        new_user = Usuarios(
            nombre_usuario=data['nombre_usuario'],
            apellido_usuario=data['apellido_usuario'],
            email=data['email'],
            telefono=data['telefono'],
            hash_contrasena_usuario=hashed_password,  # Contraseña hasheada
            metodo_de_pago=data['metodo_pago'],
            puntos=puntos.puntos_total,
            id_address=address.id_address
        )
        db.session.add(new_user)
        db.session.commit()

        logging.info("User registered successfully")
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        logging.error(f"Error during registration: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Ocurrió un error al registrar el usuario. Por favor, inténtalo de nuevo.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Ruta para iniciar sesión.

    Procesa una solicitud POST con las credenciales del usuario (correo electrónico y contraseña),
    y devuelve un token de autenticación si las credenciales son válidas.

    Returns:
        Response: Respuesta JSON con un mensaje de éxito y el token de autenticación,
                  o un mensaje de error en caso de fallo.
    """
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Recurso no encontrado"}), 404

    try:
        # Parsear los datos JSON de la solicitud
        email = data.get('email')
        password = data.get('password')

        # Llamar al método login_user del servicio de autenticación
        token = auth_service.login_user(email, password)
        return jsonify({"message": "Inicio de sesión exitoso", "token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500

@auth_bp.route('/login')
def login_page():
    return render_template('signin.html')

@auth_bp.route('/update-profile', methods=['PUT'])
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

@auth_bp.route('/change-password', methods=['PUT'])
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

@auth_bp.route('/forgot-password', methods=['POST'])
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

@auth_bp.route('/reset-password', methods=['POST'])
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