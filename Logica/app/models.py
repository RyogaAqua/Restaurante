from app import db

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    
    Id_Usuario = db.Column(db.Integer, primary_key=True)
    Nombre_Usuario = db.Column(db.String(45), nullable=False)
    Apellido_Usuario = db.Column(db.String(45), nullable=False)
    Email = db.Column(db.String(45), nullable=False, unique=True)
    Telefono = db.Column(db.String(45), nullable=True, unique=True)
    Hash_Contrasena_Usuario = db.Column(db.String(45), nullable=True)
    Fecha_Ingresada = db.Column(db.String(45), nullable=True)
    
    Puntos = db.relationship('Puntos', backref='usuario', uselist=False)
    Address = db.relationship('Address', backref='usuario', uselist=False)

class Puntos(db.Model):
    __tablename__ = 'Puntos'
    
    PuntosTotal = db.Column(db.Integer, primary_key=True)
    Redimidos = db.Column(db.Integer, nullable=True)
    Ofertas = db.Column(db.Integer, nullable=True)
    PuntosGastados = db.Column(db.Integer, nullable=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.Id_Usuario'), nullable=False)

class Address(db.Model):
    __tablename__ = 'Address'
    
    Address = db.Column(db.String(45), primary_key=True)
    Zip_code = db.Column(db.String(45), nullable=True)
    State = db.Column(db.String(45), nullable=True)
    Country = db.Column(db.String(45), nullable=True)
    City = db.Column(db.String(45), nullable=True)

class Menu_Objetos(db.Model):
    __tablename__ = 'Menu_Objetos'
    
    UPC_Objeto = db.Column(db.Integer, primary_key=True)
    Nombre_Objeto = db.Column(db.String(45), nullable=False)
    Precio = db.Column(db.Integer, nullable=True)
    Categoria = db.Column(db.String(45), nullable=False)
    Calorias = db.Column(db.Integer, nullable=True)

class Restaurante(db.Model):
    __tablename__ = 'Restaurante'
    
    Id_Restaurante = db.Column(db.Integer, primary_key=True)
    Restaurante_Address = db.Column(db.String(45), nullable=True)
    Nombre = db.Column(db.String(45), nullable=True)
    
    objetos_menu = db.relationship('Menu_Objetos', secondary='restaurante_menu', backref='restaurantes')

restaurante_menu = db.Table('restaurante_menu',
    db.Column('restaurante_id', db.Integer, db.ForeignKey('Restaurante.Id_Restaurante')),
    db.Column('objeto_id', db.Integer, db.ForeignKey('Menu_Objetos.UPC_Objeto'))
)
