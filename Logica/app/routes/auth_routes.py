from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from ..services.auth_service import AuthService  # Cambiar a import relativo
from ..database import db  # Cambiar a usar el db de database.py
from ..models import Usuarios, Address, PuntosBalance  # Cambiar a import relativo
from ..utils.security import hash_password  # Cambiar a import relativo
import logging

"""
Este módulo define las rutas relacionadas con la autenticación de usuarios,
incluyendo el inicio de sesión y el registro de nuevos usuarios.
"""

# Crear un blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()  # Instanciar el servicio de autenticación

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    # Verifica si el usuario ya existe
    if Usuarios.query.filter_by(Email=email).first():
        return jsonify({"message": "El usuario ya existe"}), 400

    # Crea un nuevo usuario
    hashed_password = generate_password_hash(password)
    nuevo_usuario = Usuarios(
        Nombre_Usuario=nombre,
        Apellido_Usuario=apellido,
        Email=email,
        Hash_Contrasena_Usuario=hashed_password
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Busca al usuario por email
    usuario = Usuarios.query.filter_by(Email=email).first()
    if not usuario or not check_password_hash(usuario.Hash_Contrasena_Usuario, password):
        return jsonify({"message": "Credenciales inválidas"}), 401

    # Genera un token (puedes usar Flask-JWT-Extended aquí)
    return jsonify({"message": "Inicio de sesión exitoso", "user_id": usuario.Id_Usuario}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Maneja el registro de nuevos usuarios.
    """
    try:
        data = request.get_json()  # Asegúrate de usar get_json para procesar JSON
        logging.info(f"Datos recibidos en la solicitud: {data}")

        # Verificar si faltan campos requeridos
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'address', 'city', 'state', 'zip_code', 'country']
        for field in required_fields:
            if not data.get(field):  # Verifica si el campo está presente y no es None
                raise ValueError(f"El campo '{field}' es obligatorio.")

        # Verificar si el usuario ya existe
        if Usuarios.query.filter_by(Email=data['email']).first():
            logging.warning("El usuario ya existe en la base de datos.")
            return jsonify({"message": "El usuario ya existe"}), 400

        # Crear una nueva dirección si no existe
        address = Address.query.filter_by(
            Address=data['address'],
            City=data['city'],
            State=data['state'],
            Zip_Code=data['zip_code'],
            Country=data['country']
        ).first()

        if not address:
            logging.info("Creando una nueva dirección en la base de datos.")
            address = Address(
                Address=data['address'],
                City=data['city'],
                State=data['state'],
                Zip_Code=data['zip_code'],
                Country=data['country']
            )
            db.session.add(address)
            db.session.commit()

        # Crear un nuevo usuario
        logging.info("Creando un nuevo usuario en la base de datos.")
        user = Usuarios(
            Nombre_Usuario=data['first_name'],
            Apellido_Usuario=data['last_name'],
            Email=data['email'],
            Telefono=data['phone'],
            Hash_Contrasena_Usuario=generate_password_hash(data['password']),
            Id_Address=address.Id_Address
        )
        db.session.add(user)
        db.session.commit()  # Commit para obtener el Id_Usuario generado

        # Crear el balance de puntos para el usuario
        logging.info("Creando el balance de puntos para el usuario.")
        puntos_balance = PuntosBalance(
            Id_Usuario=user.Id_Usuario,
            Puntos_Total=0,
            Redimidos_Total=0
        )
        db.session.add(puntos_balance)
        db.session.commit()

        logging.info("Usuario registrado exitosamente.")
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as ve:
        logging.error(f"Error durante el registro: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Error durante el registro: {e}", exc_info=True)
        return jsonify({"error": "Registration failed"}), 500

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