from app.extensions import db  # Corrected import to use extensions.py

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(45), nullable=False)
    apellido_usuario = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    telefono = db.Column(db.String(45), nullable=True, unique=True)
    hash_contrasena_usuario = db.Column(db.String(255), nullable=True)  # Increased length for hashed passwords
    fecha_ingresada = db.Column(db.String(45), nullable=True)
    
    puntos = db.relationship('Puntos', backref='usuario', uselist=False)
    address = db.relationship('Address', backref='usuario', uselist=False)
    ordenes = db.relationship('Orden', backref='usuario', lazy=True)  # Relationship with Orden

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario} {self.apellido_usuario}>"

class Puntos(db.Model):
    __tablename__ = 'Puntos'
    
    id = db.Column(db.Integer, primary_key=True)
    puntos_total = db.Column(db.Integer, nullable=False)
    redimidos = db.Column(db.Integer, nullable=True)
    ofertas = db.Column(db.Integer, nullable=True)
    puntos_gastados = db.Column(db.Integer, nullable=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f"<Puntos {self.puntos_total} for Usuario {self.usuario_id}>"

class Address(db.Model):
    __tablename__ = 'Address'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(45), nullable=True)
    state = db.Column(db.String(45), nullable=True)
    country = db.Column(db.String(45), nullable=True)
    city = db.Column(db.String(45), nullable=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f"<Address {self.address}, {self.city}, {self.state}>"

class MenuObjetos(db.Model):
    __tablename__ = 'Menu_Objetos'
    
    upc_objeto = db.Column(db.Integer, primary_key=True)
    nombre_objeto = db.Column(db.String(45), nullable=False)
    precio = db.Column(db.Float, nullable=True)  # Changed to Float for monetary values
    categoria = db.Column(db.String(45), nullable=False)
    calorias = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<MenuObjetos {self.nombre_objeto} - {self.categoria}>"

class Restaurante(db.Model):
    __tablename__ = 'Restaurante'
    
    id_restaurante = db.Column(db.Integer, primary_key=True)
    restaurante_address = db.Column(db.String(255), nullable=True)
    nombre = db.Column(db.String(45), nullable=True)
    
    objetos_menu = db.relationship('MenuObjetos', secondary='restaurante_menu', backref='restaurantes')

    def __repr__(self):
        return f"<Restaurante {self.nombre}>"

class Orden(db.Model):
    __tablename__ = 'Orden'

    id_orden = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_restaurante = db.Column(db.Integer, db.ForeignKey('Restaurante.id_restaurante'), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(45), default="Pending")  # Default status is "Pending"

    def __repr__(self):
        return f"<Orden {self.id_orden} for Usuario {self.id_usuario}>"

# Association table for Restaurante and MenuObjetos
restaurante_menu = db.Table('restaurante_menu',
    db.Column('restaurante_id', db.Integer, db.ForeignKey('Restaurante.id_restaurante')),
    db.Column('objeto_id', db.Integer, db.ForeignKey('Menu_Objetos.upc_objeto'))
)