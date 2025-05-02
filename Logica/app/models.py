from .extensions import db  # Cambiar a import relativo correcto
from sqlalchemy.orm import relationship

# Modelo para la tabla Usuarios
class Usuarios(db.Model):
    __tablename__ = 'usuarios'  # Asegúrate de que coincida con el nombre de la tabla en la base de datos

    id_usuario = db.Column('Id_Usuario', db.Integer, primary_key=True)
    puntos = db.Column('Puntos', db.Integer, nullable=False)

    # Relationships
    ordenes = db.relationship('Orden', backref='usuario')

    def __repr__(self):
        return f"<Usuario {self.id_usuario}>"

# Modelo para la tabla Address
class Address(db.Model):
    __tablename__ = 'Address'

    address = db.Column('address', db.String(45), primary_key=True)
    zip_code = db.Column('Zip_code', db.String(45))
    state = db.Column('State', db.String(45))
    country = db.Column('Country', db.String(45))
    city = db.Column('City', db.String(45))

    def __repr__(self):
        return f"<Address {self.address}, {self.city}, {self.state}>"

# Modelo para la tabla Puntos
class Puntos(db.Model):
    __tablename__ = 'Puntos'

    puntos_total = db.Column('PuntosTotal', db.Integer, primary_key=True)
    redimidos = db.Column('Redimidos', db.Integer)
    ofertas = db.Column('Ofertas', db.Integer)
    puntos_gastados = db.Column('PuntosGastados', db.Integer)

    def __repr__(self):
        return f"<Puntos {self.puntos_total}, Redimidos {self.redimidos}>"

# Modelo para la tabla PuntosBalance
class PuntosBalance(db.Model):
    __tablename__ = 'Puntos_Balance'

    user_id = db.Column(db.Integer, primary_key=True)
    puntos_total = db.Column(db.Integer, nullable=False, default=0)
    redimidos_total = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<PuntosBalance user_id={self.user_id}, puntos_total={self.puntos_total}, redimidos_total={self.redimidos_total}>"

# Modelo para la tabla Menu_Objetos
class MenuObjetos(db.Model):
    __tablename__ = 'Menu_Objetos'  # Nombre de la tabla en la base de datos
    
    id_objeto = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre_objeto = db.Column(db.String(100), nullable=False, unique=True)  # Nombre del objeto (único)
    precio = db.Column(db.Numeric(10, 2), nullable=True)  # Precio del objeto
    categoria = db.Column(db.String(45), nullable=False)  # Categoría del objeto
    calorias = db.Column(db.Integer, nullable=True)  # Calorías del objeto
    imagen_url = db.Column(db.String(255), nullable=True)  # URL de la imagen del objeto
    stock = db.Column(db.Integer, nullable=True, default=0)  # Campo para manejar el stock

    def __repr__(self):
        return f"<MenuObjetos {self.nombre_objeto} - {self.categoria}, Stock: {self.stock}>"

# Modelo para la tabla Orden
class Orden(db.Model):
    __tablename__ = 'Orden'

    id_transaccion = db.Column('Id_Transaccion', db.Integer, primary_key=True)
    id_usuario = db.Column('Id_Usuario', db.Integer, nullable=False)
    puntos = db.Column('Puntos', db.Integer, nullable=False)
    address = db.Column('Address', db.String(45), nullable=False)
    objetos = db.Column('Objetos', db.Integer, nullable=False)

    # Corrected composite foreign key linking to Usuarios and Address
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['id_usuario', 'puntos'],
            ['usuarios.Id_Usuario', 'usuarios.Puntos']
        ),
        db.ForeignKeyConstraint(
            ['address'],
            ['Address.address']
        ),
        db.ForeignKeyConstraint(
            ['objetos'],
            ['Menu_Objetos.id_objeto']
        ),
    )

    # Relationships
    menu_objeto = db.relationship('MenuObjetos', backref='ordenes')

    def __repr__(self):
        return f"<Orden {self.id_transaccion} for Usuario {self.id_usuario}>"

# Modelo para la tabla Orden_Items
class OrdenItems(db.Model):
    __tablename__ = 'Orden_Items'  # Nombre de la tabla en la base de datos

    id_orden_item = db.Column(db.Integer, primary_key=True)  # Clave primaria
    id_transaccion = db.Column(db.Integer, db.ForeignKey('Orden.id_transaccion'), nullable=False)  # Clave foránea a Orden
    id_objeto = db.Column(db.Integer, db.ForeignKey('Menu_Objetos.id_objeto'), nullable=False)  # Clave foránea a Menu_Objetos
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Cantidad del objeto
    precio_unitario_congelado = db.Column(db.Numeric(10, 2), nullable=False)  # Precio unitario al momento de la orden

    def __repr__(self):
        return f"<OrdenItems Orden {self.id_transaccion}, Objeto {self.id_objeto}>"

# Modelo para la tabla CartItem
class CartItem(db.Model):
    __tablename__ = 'CartItem'  # Nombre de la tabla en la base de datos

    id_cart_item = db.Column(db.Integer, primary_key=True)  # Clave primaria
    user_id = db.Column(db.Integer, nullable=False)  # ID del usuario
    id_objeto = db.Column(db.Integer, db.ForeignKey('Menu_Objetos.id_objeto'), nullable=False)  # Clave foránea a Menu_Objetos
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Cantidad del objeto

    # Relación con MenuObjetos
    menu_objeto = db.relationship('MenuObjetos', backref='cart_items')

    def __repr__(self):
        return f"<CartItem Usuario {self.user_id}, Objeto {self.id_objeto}, Cantidad {self.quantity}>"

# Modelo para la tabla Notification
class Notification(db.Model):
    __tablename__ = 'Notification'  # Nombre de la tabla en la base de datos

    id_notification = db.Column(db.Integer, primary_key=True)  # Clave primaria
    user_id = db.Column(db.Integer, nullable=False)  # ID del usuario
    message = db.Column(db.String(255), nullable=False)  # Mensaje de la notificación
    type = db.Column(db.String(20), nullable=False, default='info')  # Tipo de notificación (info, success, error)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Fecha de creación

    def to_dict(self):
        """
        Convierte el objeto Notification a un diccionario.

        Returns:
            dict: Representación del objeto Notification.
        """
        return {
            "id_notification": self.id_notification,
            "user_id": self.user_id,
            "message": self.message,
            "type": self.type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Notification Usuario {self.user_id}, Tipo {self.type}>"

# Modelo para la tabla SupportMessage
class SupportMessage(db.Model):
    __tablename__ = 'SupportMessage'  # Nombre de la tabla en la base de datos

    id_message = db.Column(db.Integer, primary_key=True)  # Clave primaria
    user_id = db.Column(db.Integer, nullable=False)  # ID del usuario
    subject = db.Column(db.String(255), nullable=False)  # Asunto del mensaje
    message = db.Column(db.Text, nullable=False)  # Contenido del mensaje
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Fecha de creación

    def to_dict(self):
        """
        Convierte el objeto SupportMessage a un diccionario.

        Returns:
            dict: Representación del objeto SupportMessage.
        """
        return {
            "id_message": self.id_message,
            "user_id": self.user_id,
            "subject": self.subject,
            "message": self.message,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<SupportMessage Usuario {self.user_id}, Asunto {self.subject}>"