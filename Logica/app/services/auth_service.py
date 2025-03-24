import bcrypt
import jwt
import datetime
from app.models import Usuario
from app.config import SECRET_KEY

class AuthService:

    def __init__(self):
        self.secret_key = SECRET_KEY
        self.expiration_time = 3600  # 1 hora

    # Método para registrar un nuevo usuario
    def register_user(self, nombre_usuario, apellido_usuario, email, telefono, contrasena, address, metodo_pago):
        # Verificar si el email ya existe en la base de datos
        if Usuario.query.filter_by(email=email).first():
            raise ValueError("El email ya está registrado.")
        
        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        # Crear un nuevo usuario en la base de datos
        new_user = Usuario(
            Nombre_Usuario=nombre_usuario,
            Apellido_Usuario=apellido_usuario,
            Email=email,
            Telefono=telefono,
            Hash_Contrasena_Usuario=hashed_password.decode('utf-8'),
            MetodoDePago=metodo_pago,
            Address=address,
            Puntos=0  # Puntos iniciales
        )

        # Guardar el usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Usuario registrado con éxito"}

    # Método para iniciar sesión (login) de un usuario
    def login_user(self, email, contrasena):
        # Buscar al usuario por email
        user = Usuario.query.filter_by(email=email).first()
        
        if not user:
            raise ValueError("El usuario no existe.")
        
        # Verificar la contraseña
        if not bcrypt.checkpw(contrasena.encode('utf-8'), user.Hash_Contrasena_Usuario.encode('utf-8')):
            raise ValueError("Contraseña incorrecta.")
        
        # Crear un token JWT
        token = self.create_jwt_token(user)

        return {"message": "Inicio de sesión exitoso", "token": token}

    # Crear un JWT para la autenticación
    def create_jwt_token(self, user):
        # Definir la fecha de expiración del token
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expiration_time)

        # Crear el payload del JWT
        payload = {
            "sub": user.Id_Usuario,
            "email": user.Email,
            "exp": expiration_date
        }

        # Crear el token JWT
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")

        return token

    # Método para validar el token JWT
    def validate_jwt_token(self, token):
        try:
            # Decodificar el token
            decoded_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise ValueError("El token ha expirado.")
        except jwt.InvalidTokenError:
            raise ValueError("El token no es válido.")
