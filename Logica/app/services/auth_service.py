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
        from ..models import Usuario  # Importación diferida para evitar dependencia circular
        new_user = Usuario(
            nombre_usuario=data.get('nombre_usuario'),
            apellido_usuario=data.get('apellido_usuario'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            hash_contrasena_usuario=data.get('hash_contrasena_usuario'),
            fecha_ingresada=data.get('fecha_ingresada')
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user