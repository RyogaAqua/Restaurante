from app.extensions import db  # Importa la instancia de la base de datos desde extensions.py

# Modelo para la tabla Usuarios
class Usuario(db.Model):
    __tablename__ = 'Usuarios'  # Nombre de la tabla en la base de datos
    
    id_usuario = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre_usuario = db.Column(db.String(45), nullable=False)  # Nombre del usuario (obligatorio)
    apellido_usuario = db.Column(db.String(45), nullable=False)  # Apellido del usuario (obligatorio)
    email = db.Column(db.String(45), nullable=False, unique=True)  # Correo electrónico (obligatorio y único)
    telefono = db.Column(db.String(45), nullable=True, unique=True)  # Teléfono (opcional y único)
    hash_contrasena_usuario = db.Column(db.String(255), nullable=True)  # Contraseña en formato hash (opcional)
    fecha_ingresada = db.Column(db.String(45), nullable=True)  # Fecha asociada al usuario (opcional)
    
    # Relación uno a uno con Puntos
    puntos = db.relationship('Puntos', backref='usuario', uselist=False)
    # Relación uno a uno con Address
    address = db.relationship('Address', backref='usuario', uselist=False)
    # Relación uno a muchos con Orden
    ordenes = db.relationship('Orden', backref='usuario', lazy=True)

    def __repr__(self):
        # Representación en texto del modelo
        return f"<Usuario {self.nombre_usuario} {self.apellido_usuario}>"

# Modelo para la tabla Puntos
class Puntos(db.Model):
    __tablename__ = 'Puntos'  # Nombre de la tabla en la base de datos
    
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    puntos_total = db.Column(db.Integer, nullable=False)  # Total de puntos acumulados (obligatorio)
    redimidos = db.Column(db.Integer, nullable=True)  # Puntos redimidos (opcional)
    ofertas = db.Column(db.Integer, nullable=True)  # Ofertas asociadas a los puntos (opcional)
    puntos_gastados = db.Column(db.Integer, nullable=True)  # Puntos gastados (opcional)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)  # Clave foránea a Usuarios

    def __repr__(self):
        # Representación en texto del modelo
        return f"<Puntos {self.puntos_total} for Usuario {self.usuario_id}>"

# Modelo para la tabla Address
class Address(db.Model):
    __tablename__ = 'Address'  # Nombre de la tabla en la base de datos
    
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    address = db.Column(db.String(255), nullable=False)  # Dirección completa (obligatoria)
    zip_code = db.Column(db.String(45), nullable=True)  # Código postal (opcional)
    state = db.Column(db.String(45), nullable=True)  # Estado o provincia (opcional)
    country = db.Column(db.String(45), nullable=True)  # País (opcional)
    city = db.Column(db.String(45), nullable=True)  # Ciudad (opcional)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)  # Clave foránea a Usuarios

    def __repr__(self):
        # Representación en texto del modelo
        return f"<Address {self.address}, {self.city}, {self.state}>"

# Modelo para la tabla Menu_Objetos
class MenuObjetos(db.Model):
    __tablename__ = 'Menu_Objetos'  # Nombre de la tabla en la base de datos
    
    upc_objeto = db.Column(db.Integer, primary_key=True)  # Clave primaria (código único del objeto)
    nombre_objeto = db.Column(db.String(45), nullable=False)  # Nombre del objeto en el menú (obligatorio)
    precio = db.Column(db.Float, nullable=True)  # Precio del objeto (opcional)
    categoria = db.Column(db.String(45), nullable=False)  # Categoría del objeto (obligatoria)
    calorias = db.Column(db.Integer, nullable=True)  # Calorías del objeto (opcional)

    def __repr__(self):
        # Representación en texto del modelo
        return f"<MenuObjetos {self.nombre_objeto} - {self.categoria}>"

# Modelo para la tabla Restaurante
class Restaurante(db.Model):
    __tablename__ = 'Restaurante'  # Nombre de la tabla en la base de datos
    
    id_restaurante = db.Column(db.Integer, primary_key=True)  # Clave primaria
    restaurante_address = db.Column(db.String(255), nullable=True)  # Dirección del restaurante (opcional)
    nombre = db.Column(db.String(45), nullable=True)  # Nombre del restaurante (opcional)
    
    # Relación muchos a muchos con MenuObjetos a través de la tabla intermedia restaurante_menu
    objetos_menu = db.relationship('MenuObjetos', secondary='restaurante_menu', backref='restaurantes')

    def __repr__(self):
        # Representación en texto del modelo
        return f"<Restaurante {self.nombre}>"

# Modelo para la tabla Orden
class Orden(db.Model):
    __tablename__ = 'Orden'  # Nombre de la tabla en la base de datos

    id_orden = db.Column(db.Integer, primary_key=True)  # Clave primaria
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)  # Clave foránea a Usuarios
    id_restaurante = db.Column(db.Integer, db.ForeignKey('Restaurante.id_restaurante'), nullable=False)  # Clave foránea a Restaurante
    puntos = db.Column(db.Integer, nullable=False)  # Puntos utilizados en la orden (obligatorio)
    precio_total = db.Column(db.Float, nullable=False)  # Precio total de la orden (obligatorio)
    direccion = db.Column(db.String(255), nullable=False)  # Dirección de entrega (obligatoria)
    estado = db.Column(db.String(45), default="Pending")  # Estado de la orden (por defecto "Pending")

    def __repr__(self):
        # Representación en texto del modelo
        return f"<Orden {self.id_orden} for Usuario {self.id_usuario}>"

# Tabla intermedia para la relación muchos a muchos entre Restaurante y MenuObjetos
restaurante_menu = db.Table('restaurante_menu',
    db.Column('restaurante_id', db.Integer, db.ForeignKey('Restaurante.id_restaurante')),  # Clave foránea a Restaurante
    db.Column('objeto_id', db.Integer, db.ForeignKey('Menu_Objetos.upc_objeto'))  # Clave foránea a MenuObjetos
)