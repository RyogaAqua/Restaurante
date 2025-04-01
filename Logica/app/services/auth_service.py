from app.extensions import db  # Import db from extensions.py

class AuthService:
    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.
        :param email: The email address of the user.
        :return: The user object or None if not found.
        """
        from ..models import Usuario  # Delay the import to avoid circular dependency
        return Usuario.query.filter_by(email=email).first()

    def create_user(self, data):
        """
        Create a new user in the database.
        :param data: Dictionary containing user details.
        :return: The newly created user object.
        """
        from ..models import Usuario  # Delay the import to avoid circular dependency
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