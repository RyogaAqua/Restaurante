from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy import func  # Importa func para usar sa.func.now()
from .extensions import db
from flask_login import UserMixin

class Address(db.Model):
    __tablename__ = 'Address'

    Id_Address = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Address = db.Column(db.String(255), nullable=False)
    Zip_Code = db.Column(db.String(20), nullable=True)
    State = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(100), nullable=True)
    City = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Address(Id_Address={self.Id_Address}, Address='{self.Address}', City='{self.City}')>"


class Usuarios(db.Model, UserMixin):
    __tablename__ = 'Usuarios'

    Id_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Usuario = db.Column(db.String(45), nullable=False)
    Apellido_Usuario = db.Column(db.String(45), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Telefono = db.Column(db.String(25), unique=True, nullable=True)
    Hash_Contrasena_Usuario = db.Column(db.String(255), nullable=True)
    Fecha_Ingresada = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    MetodoDePago = db.Column(db.String(45), nullable=True)
    Id_Address = db.Column(db.Integer, db.ForeignKey('Address.Id_Address'), nullable=True)

    puntos_balance = db.relationship('PuntosBalance', back_populates='usuario', uselist=False)
    ordenes = db.relationship('Orden', back_populates='usuario')  # Relación con Orden
    cart_items = db.relationship('CartItem', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Usuarios(Id_Usuario={self.Id_Usuario}, Email='{self.Email}')>"

    def get_id(self):
        return str(self.Id_Usuario)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


class PuntosBalance(db.Model):
    __tablename__ = 'Puntos_Balance'

    Id_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.Id_Usuario'), primary_key=True, nullable=False)
    Puntos_Total = db.Column(db.Integer, nullable=False, default=0)
    Redimidos_Total = db.Column(db.Integer, nullable=False, default=0)
    Actualizado_En = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    usuario = db.relationship('Usuarios', back_populates='puntos_balance')


class MenuObjetos(db.Model):
    __tablename__ = 'menu_objetos'

    Id_Objeto = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for the menu item')
    Nombre_Objeto = Column(String(100), nullable=False, unique=True, comment='Name of the menu item (must be unique globally)')
    Precio = Column(Float, comment='Price of the menu item')
    Categoria = Column(String(45), nullable=False, comment='Category of the item (e.g., Appetizer, Main, Drink)')
    Calorias = Column(Integer, comment='Calorie count for the item')
    Imagen_URL = Column(String(255), comment='URL or path to the menu item image')

    # Relación inversa con OrdenItems
    orden_items = relationship('OrdenItems', back_populates='menu_objeto')


class Orden(db.Model):
    __tablename__ = 'Orden'

    Id_Orden = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.Id_Usuario'), nullable=False)
    Id_Delivery_Address = db.Column(db.Integer, db.ForeignKey('Address.Id_Address'), nullable=False)
    Precio_Total = db.Column(db.Numeric(10, 2), nullable=True)
    Puntos_Gastados = db.Column(db.Integer, nullable=True, default=0)
    Puntos_Ganados = db.Column(db.Integer, nullable=True, default=0)
    Fecha_Orden = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    usuario = db.relationship('Usuarios', back_populates='ordenes')  # Relación con Usuarios
    delivery_address = db.relationship('Address')  # Relación con Address
    orden_items = relationship('OrdenItems', back_populates='orden')


class OrdenItems(db.Model):
    __tablename__ = 'orden_items'

    Id_Orden_Item = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for this specific line item in an order')
    Id_Orden = Column(Integer, ForeignKey('Orden.Id_Orden'), nullable=False, comment='Foreign key linking to the order header')
    Id_Objeto = Column(Integer, ForeignKey('menu_objetos.Id_Objeto'), nullable=False, comment='Foreign key linking to the menu item ordered')
    Quantity = Column(Integer, nullable=False, default=1, comment='Number of this specific item ordered')
    Precio_Unitario_Congelado = Column(Float, nullable=False, comment='Price of the item unit at the time the order was placed')

    # Relación con Orden y MenuObjetos
    orden = relationship('Orden', back_populates='orden_items')
    menu_objeto = relationship('MenuObjetos', back_populates='orden_items')


class CartItem(db.Model):
    __tablename__ = 'cart'

    Id_Cart = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.Id_Usuario'), nullable=False)
    Id_Objeto = db.Column(db.Integer, nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False, default=1)
    Agregado_En = db.Column(db.TIMESTAMP, nullable=True, server_default=db.func.current_timestamp())

    user = db.relationship('Usuarios', back_populates='cart_items')