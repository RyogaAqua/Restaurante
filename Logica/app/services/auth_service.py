from app.extensions import db  # Importa db desde extensions.py

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
            Usuario: El objeto del usuario si se encuentra, o None si no existe.
        """
        from ..models import Usuario  # Importación diferida para evitar dependencia circular
        return Usuario.query.filter_by(email=email).first()

    def create_user(self, data):
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            data (dict): Diccionario que contiene los detalles del usuario.

        Returns:
            Usuario: El objeto del usuario recién creado.
        """
        from ..models import Usuario, Address  # Importación diferida para evitar dependencia circular

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
        new_user = Usuario(
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
            Usuario: El objeto del usuario actualizado.
        """
        from ..models import Usuario  # Importación diferida para evitar dependencia circular
        user = Usuario.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")

        user.metodo_de_pago = metodo_de_pago
        db.session.commit()
        return user