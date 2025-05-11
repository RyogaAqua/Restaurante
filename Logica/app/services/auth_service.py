from ..extensions import db  # Import relativo correcto
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

class AuthService:
    """
    Servicio para manejar la lógica relacionada con la autenticación de usuarios.
    """

    def get_user_by_email(self, email):
        """
        Recupera un usuario por su dirección de correo electrónico.

        Args:
            email (str): La dirección de correo electrónico del usuario.

        Returns:
            Usuarios: El objeto del usuario si se encuentra, o None si no existe.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular
        return Usuarios.query.filter_by(Email=email).first()

    def create_user(self, data):
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            data (dict): Diccionario que contiene los detalles del usuario.

        Returns:
            Usuarios: El objeto del usuario recién creado.
        """
        from ..models import Usuarios, Address  # Importación diferida para evitar dependencia circular

        # Crear o buscar la dirección asociada
        address_data = data.get('address')
        if address_data:
            address = Address.query.filter_by(
                address=address_data.get('address'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                zip_code=address_data.get('zip_code'),
                country=address_data.get('country')
            ).first()

            if not address:
                address = Address(
                    address=address_data.get('address'),
                    city=address_data.get('city'),
                    state=address_data.get('state'),
                    zip_code=address_data.get('zip_code'),
                    country=address_data.get('country')
                )
                db.session.add(address)
                db.session.flush()  # Asegura que la dirección tenga un ID antes de usarla
        else:
            address = None

        # Crear el usuario
        new_user = Usuarios(
            nombre_usuario=data.get('nombre_usuario'),
            apellido_usuario=data.get('apellido_usuario'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            hash_contrasena_usuario=data.get('hash_contrasena_usuario'),
            metodo_de_pago=data.get('metodo_de_pago'),
            id_address=address.id_address if address else None
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_user_payment_method(self, user_id, metodo_de_pago):
        """
        Actualiza el método de pago de un usuario.

        Args:
            user_id (int): ID del usuario.
            metodo_de_pago (str): Nuevo método de pago.

        Returns:
            Usuarios: El objeto del usuario actualizado.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular
        user = Usuarios.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")

        user.metodo_de_pago = metodo_de_pago
        db.session.commit()
        return user

    def update_user_profile(self, user_id, updated_data):
        """
        Actualiza el perfil del usuario en la base de datos.

        Args:
            user_id (int): ID del usuario.
            updated_data (dict): Diccionario con los datos actualizados del usuario.

        Returns:
            dict: Datos actualizados del usuario.

        Raises:
            ValueError: Si el usuario no existe o ocurre un error durante la actualización.
        """
        from ..models import Usuarios, Address  # Importación diferida para evitar dependencia circular
        try:
            user = Usuarios.query.get(user_id)
            if not user:
                raise ValueError("Usuario no encontrado.")

            # Actualizar los datos del usuario
            user.nombre_usuario = updated_data.get('nombre_usuario', user.nombre_usuario)
            user.apellido_usuario = updated_data.get('apellido_usuario', user.apellido_usuario)
            user.email = updated_data.get('email', user.email)
            user.telefono = updated_data.get('telefono', user.telefono)

            # Actualizar o crear la dirección
            address_data = updated_data.get('address')
            if address_data:
                address = Address.query.filter_by(
                    address=address_data.get('address'),
                    city=address_data.get('city'),
                    state=address_data.get('state'),
                    zip_code=address_data.get('zip_code'),
                    country=address_data.get('country')
                ).first()

                if not address:
                    address = Address(
                        address=address_data.get('address'),
                        city=address_data.get('city'),
                        state=address_data.get('state'),
                        zip_code=address_data.get('zip_code'),
                        country=address_data.get('country')
                    )
                    db.session.add(address)
                    db.session.flush()  # Asegura que la dirección tenga un ID antes de usarla

                user.id_address = address.id_address

            db.session.commit()
            return {
                "id_usuario": user.id_usuario,
                "nombre_usuario": user.nombre_usuario,
                "apellido_usuario": user.apellido_usuario,
                "email": user.email,
                "telefono": user.telefono,
                "address": address.to_dict() if address else None
            }
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al actualizar el perfil del usuario: {e}")

    def change_user_password(self, user_id, current_password, new_password):
        """
        Cambia la contraseña de un usuario después de validar la contraseña actual.

        Args:
            user_id (int): ID del usuario.
            current_password (str): Contraseña actual del usuario.
            new_password (str): Nueva contraseña del usuario.

        Raises:
            ValueError: Si la contraseña actual no coincide o si ocurre un error.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular
        try:
            user = Usuarios.query.get(user_id)
            if not user:
                raise ValueError("Usuario no encontrado.")

            # Validar la contraseña actual
            if not check_password_hash(user.hash_contrasena_usuario, current_password):
                raise ValueError("La contraseña actual es incorrecta.")

            # Generar el hash de la nueva contraseña
            user.hash_contrasena_usuario = generate_password_hash(new_password)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al cambiar la contraseña: {e}")

    def send_password_reset_email(self, email):
        """
        Envía un correo electrónico con un enlace para restablecer la contraseña.

        Args:
            email (str): Correo electrónico del usuario.

        Raises:
            ValueError: Si el usuario no existe.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular
        user = self.get_user_by_email(email)
        if not user:
            raise ValueError("No se encontró un usuario con ese correo electrónico.")

        # Generar un token de restablecimiento
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset-salt')

        # Construir el enlace de restablecimiento
        reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={token}"

        # Enviar el correo (simulado aquí, reemplazar con integración real)
        print(f"Enlace de restablecimiento de contraseña: {reset_url}")

    def reset_password(self, token, new_password):
        """
        Restablece la contraseña del usuario utilizando un token de restablecimiento.

        Args:
            token (str): Token de restablecimiento de contraseña.
            new_password (str): Nueva contraseña del usuario.

        Raises:
            ValueError: Si el token es inválido o ha expirado.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        try:
            # Validar el token
            email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hora de validez
            user = self.get_user_by_email(email)
            if not user:
                raise ValueError("Usuario no encontrado.")

            # Actualizar la contraseña
            user.hash_contrasena_usuario = generate_password_hash(new_password)
            db.session.commit()
        except Exception as e:
            raise ValueError("El token es inválido o ha expirado.")

    def login_user(self, email, password):
        """
        Autentica a un usuario verificando su correo electrónico y contraseña.

        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            str: Token de autenticación si las credenciales son válidas.

        Raises:
            ValueError: Si las credenciales son inválidas o el usuario no existe.
        """
        from ..models import Usuarios  # Importación diferida para evitar dependencia circular

        # Buscar al usuario por correo electrónico
        user = Usuarios.query.filter_by(Email=email).first()
        if not user:
            raise ValueError("Usuario no encontrado.")

        # Verificar la contraseña
        if not check_password_hash(user.Hash_Contrasena_Usuario, password):
            raise ValueError("Contraseña incorrecta.")

        # Generar un token de autenticación (simulado aquí, reemplazar con JWT real si es necesario)
        token = f"fake-token-for-{user.Id_Usuario}"
        return token

    def validate_user(self, email, password):
        """
        Valida las credenciales del usuario.

        Args:
            email (str): La dirección de correo electrónico del usuario.
            password (str): La contraseña del usuario.

        Returns:
            Usuarios: El objeto del usuario si las credenciales son correctas, o None si no lo son.
        """
        user = self.get_user_by_email(email)
        if user and check_password_hash(user.Hash_Contrasena_Usuario, password):
            return user
        return None