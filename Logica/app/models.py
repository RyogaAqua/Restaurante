from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy import func  # Importa func para usar sa.func.now()
from .database import Base

class Address(Base):
    __tablename__ = 'address'

    Id_Address = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for the address')
    Address = Column(String(255), nullable=False, comment='Street address line(s)')
    Zip_Code = Column(String(20), comment='Postal or Zip code')
    State = Column(String(100), comment='State, Province, or Region')
    Country = Column(String(100), comment='Country')
    City = Column(String(100), comment='City or Town')

    # Relación inversa con Usuarios y Orden
    usuarios = relationship('Usuarios', back_populates='address')
    ordenes = relationship('Orden', back_populates='address')


class Usuarios(Base):
    __tablename__ = 'usuarios'

    Id_Usuario = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for the user')
    Nombre_Usuario = Column(String(45), nullable=False, comment="User's first name")
    Apellido_Usuario = Column(String(45), nullable=False, comment="User's last name")
    Email = Column(String(100), nullable=False, unique=True, comment="User's email address (must be unique)")
    Telefono = Column(String(25), unique=True, comment="User's phone number (must be unique if provided)")
    Hash_Contrasena_Usuario = Column(String(255), comment="Hashed user password")
    Fecha_Ingresada = Column(DateTime, server_default=func.now(), comment="Date and time when the user account was created")
    MetodoDePago = Column(String(45), comment="Preferred payment method information")
    Id_Address = Column(Integer, ForeignKey('address.Id_Address'), comment="Foreign key to the user's default address in the Address table")

    # Relación con Address y Puntos_Balance
    address = relationship('Address', back_populates='usuarios')
    puntos_balance = relationship('PuntosBalance', uselist=False, back_populates='usuario')


class PuntosBalance(Base):
    __tablename__ = 'puntos_balance'

    Id_Usuario = Column(Integer, ForeignKey('usuarios.Id_Usuario'), primary_key=True, comment='Foreign key linking to the user; also Primary Key')
    Puntos_Total = Column(Integer, nullable=False, default=0, comment='Current available points balance')
    Redimidos_Total = Column(Integer, nullable=False, default=0, comment='Lifetime total points redeemed by the user')
    Actualizado_En = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='Timestamp of the last balance update')

    # Relación con Usuarios
    usuario = relationship('Usuarios', back_populates='puntos_balance')


class MenuObjetos(Base):
    __tablename__ = 'menu_objetos'

    Id_Objeto = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for the menu item')
    Nombre_Objeto = Column(String(100), nullable=False, unique=True, comment='Name of the menu item (must be unique globally)')
    Precio = Column(Float, comment='Price of the menu item')
    Categoria = Column(String(45), nullable=False, comment='Category of the item (e.g., Appetizer, Main, Drink)')
    Calorias = Column(Integer, comment='Calorie count for the item')
    Imagen_URL = Column(String(255), comment='URL or path to the menu item image')

    # Relación inversa con OrdenItems
    orden_items = relationship('OrdenItems', back_populates='menu_objeto')


class Orden(Base):
    __tablename__ = 'orden'

    Id_Orden = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for the order transaction')
    Id_Usuario = Column(Integer, ForeignKey('usuarios.Id_Usuario'), nullable=False, comment='Foreign key linking to the user who placed the order')
    Id_Delivery_Address = Column(Integer, ForeignKey('address.Id_Address'), nullable=False, comment='Foreign key linking to the address for this specific order delivery')
    Precio_Total = Column(Float, comment='Calculated total price for the order')
    Puntos_Gastados = Column(Integer, default=0, comment='Points redeemed by the user for this order')
    Puntos_Ganados = Column(Integer, default=0, comment='Points earned by the user from this order')
    Fecha_Orden = Column(DateTime, nullable=False, server_default=func.now(), comment='Date and time when the order was placed')

    # Relación con Usuarios, Address y OrdenItems
    usuario = relationship('Usuarios')
    address = relationship('Address', back_populates='ordenes')
    orden_items = relationship('OrdenItems', back_populates='orden')


class OrdenItems(Base):
    __tablename__ = 'orden_items'

    Id_Orden_Item = Column(Integer, primary_key=True, autoincrement=True, comment='Unique identifier for this specific line item in an order')
    Id_Orden = Column(Integer, ForeignKey('orden.Id_Orden'), nullable=False, comment='Foreign key linking to the order header')
    Id_Objeto = Column(Integer, ForeignKey('menu_objetos.Id_Objeto'), nullable=False, comment='Foreign key linking to the menu item ordered')
    Quantity = Column(Integer, nullable=False, default=1, comment='Number of this specific item ordered')
    Precio_Unitario_Congelado = Column(Float, nullable=False, comment='Price of the item unit at the time the order was placed')

    # Relación con Orden y MenuObjetos
    orden = relationship('Orden', back_populates='orden_items')
    menu_objeto = relationship('MenuObjetos', back_populates='orden_items')