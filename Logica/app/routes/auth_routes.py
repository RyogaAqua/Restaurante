from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..services.auth_service import AuthService  # Cambiar a import relativo
from ..extensions import db  # Use the db instance from extensions.py
from ..models import Usuarios, Address, PuntosBalance  # Cambiar a import relativo
from ..utils.security import hash_password  # Cambiar a import relativo
import logging
import traceback
from flask_login import current_user, login_user, logout_user

logging.basicConfig(level=logging.DEBUG)
logging.debug("Cargando el endpoint /status en el Blueprint auth_bp")

"""
Este módulo define las rutas relacionadas con la autenticación de usuarios,
incluyendo el inicio de sesión y el registro de nuevos usuarios.
"""

# Crear un blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()  # Instanciar el servicio de autenticación

@auth_bp.route('/signup', methods=['POST'])
def signup():
    logging.info("Received signup request.")
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        nombre = data.get('nombre')
        apellido = data.get('apellido')

        logging.debug(f"Signup payload: {data}")

        # Validate required fields
        if not all([email, password, nombre, apellido]):
            logging.error("Missing required fields in signup payload.")
            return jsonify({"error": "Todos los campos son obligatorios."}), 400

        # Check if the user already exists
        if Usuarios.query.filter_by(Email=email).first():
            logging.warning(f"User with email {email} already exists.")
            return jsonify({"message": "El usuario ya existe"}), 400

        # Create a new user
        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuarios(
            Nombre_Usuario=nombre,
            Apellido_Usuario=apellido,
            Email=email,
            Hash_Contrasena_Usuario=hashed_password
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        logging.info(f"User {email} created successfully.")
        return jsonify({"message": "Usuario creado exitosamente"}), 201

    except Exception as e:
        logging.error(f"Error during signup: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Ocurrió un error inesperado."}), 500


@auth_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logging.error("El campo 'email' o 'password' está vacío.")
            return jsonify({"error": "Email y contraseña son obligatorios."}), 400

        # Busca al usuario por email
        usuario = Usuarios.query.filter_by(Email=email).first()
        if not usuario:
            logging.warning(f"Usuario con email {email} no encontrado.")
            return jsonify({"error": "Credenciales inválidas."}), 401

        # Verifica la contraseña
        if not check_password_hash(usuario.Hash_Contrasena_Usuario, password):
            logging.warning("Contraseña incorrecta para el usuario.")
            return jsonify({"error": "Credenciales inválidas."}), 401

        # Genera un token (puedes usar Flask-JWT-Extended aquí)
        logging.info(f"Usuario {email} inició sesión exitosamente.")
        return jsonify({"message": "Inicio de sesión exitoso", "user_id": usuario.Id_Usuario}), 200

    except Exception as e:
        logging.error(f"Error durante el inicio de sesión: {e}\nDatos ingresados: email={data.get('email')}, password={'*' * len(data.get('password', ''))}", exc_info=True)
        return jsonify({"error": "Ocurrió un error inesperado."}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Maneja el registro de nuevos usuarios.
    """
    try:
        data = request.get_json()  # Asegúrate de usar get_json para procesar JSON
        logging.info(f"Datos recibidos en la solicitud: {data}")

        # Verificar si faltan campos requeridos
        required_fields = ['Nombre_Usuario', 'Apellido_Usuario', 'Email', 'Telefono', 'Hash_Contrasena_Usuario', 'address', 'city', 'state', 'zip_code', 'country', 'MetodoDePago']
        for field in required_fields:
            if not data.get(field):  # Verifica si el campo está presente y no es None
                logging.error(f"El campo '{field}' es obligatorio y no fue proporcionado.")
                raise ValueError(f"El campo '{field}' es obligatorio.")

        # Verificar si el usuario ya existe
        if Usuarios.query.filter_by(Email=data['Email']).first():
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
            Nombre_Usuario=data['Nombre_Usuario'],
            Apellido_Usuario=data['Apellido_Usuario'],
            Email=data['Email'],
            Telefono=data['Telefono'],
            Hash_Contrasena_Usuario=generate_password_hash(data['Hash_Contrasena_Usuario']),
            Fecha_Ingresada=db.func.now(),  # Fecha actual
            MetodoDePago=data['MetodoDePago'],
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
    """
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        logging.error("Faltan campos obligatorios en la solicitud de inicio de sesión.")
        return jsonify({"error": "Recurso no encontrado"}), 404

    try:
        email = data.get('email')
        password = data.get('password')

        logging.debug(f"Intentando iniciar sesión con email: {email}")

        # Validar las credenciales del usuario
        user = auth_service.validate_user(email, password)
        if user:
            login_user(user)  # Establecer la sesión del usuario
            session['user_id'] = user.Id_Usuario  # Configurar manualmente el ID del usuario en la sesión
            logging.info(f"Inicio de sesión exitoso para el usuario: {email}")
            return jsonify({"message": "Inicio de sesión exitoso"}), 200
        else:
            logging.warning("Credenciales inválidas.")
            return jsonify({"error": "Credenciales inválidas"}), 401
    except Exception as e:
        logging.error(f"Error durante el inicio de sesión: {e}", exc_info=True)
        return jsonify({"error": "Error interno del servidor"}), 500

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

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    logging.debug("Endpoint /status llamado")
    if current_user.is_authenticated:
        return jsonify({'isAuthenticated': True, 'username': current_user.Nombre_Usuario})
    else:
        return jsonify({'isAuthenticated': False})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    logging.info("Usuario ha cerrado sesión exitosamente.")
    return jsonify({"message": "Cierre de sesión exitoso."}), 200