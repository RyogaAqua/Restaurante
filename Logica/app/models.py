from .extensions import db  # Cambiar a import relativo correcto

# Modelo para la tabla Usuarios
class Usuario(db.Model):
    __tablename__ = 'Usuarios'  # Nombre de la tabla en la base de datos
    
    id_usuario = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre_usuario = db.Column(db.String(45), nullable=False)  # Nombre del usuario (obligatorio)
    apellido_usuario = db.Column(db.String(45), nullable=False)  # Apellido del usuario (obligatorio)
    email = db.Column(db.String(100), nullable=False, unique=True)  # Correo electrónico (obligatorio y único)
    telefono = db.Column(db.String(25), nullable=True, unique=True)  # Teléfono (opcional y único)
    hash_contrasena_usuario = db.Column(db.String(255), nullable=True)  # Contraseña en formato hash (opcional)
    fecha_ingresada = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())  # Fecha de creación
    metodo_de_pago = db.Column(db.String(45), nullable=True)  # Método de pago preferido (opcional)
    id_address = db.Column(db.Integer, db.ForeignKey('Address.id_address'), nullable=True)  # Clave foránea a Address
    
    # Relación uno a uno con Puntos
    puntos_balance = db.relationship('PuntosBalance', backref='usuario', uselist=False)
    # Relación uno a muchos con Orden
    ordenes = db.relationship('Orden', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario} {self.apellido_usuario}>"

# Modelo para la tabla Address
class Address(db.Model):
    __tablename__ = 'Address'  # Nombre de la tabla en la base de datos
    
    id_address = db.Column(db.Integer, primary_key=True)  # Clave primaria
    address = db.Column(db.String(255), nullable=False)  # Dirección completa (obligatoria)
    zip_code = db.Column(db.String(20), nullable=True)  # Código postal (opcional)
    state = db.Column(db.String(100), nullable=True)  # Estado o provincia (opcional)
    country = db.Column(db.String(100), nullable=True)  # País (opcional)
    city = db.Column(db.String(100), nullable=True)  # Ciudad (opcional)

    def __repr__(self):
        return f"<Address {self.address}, {self.city}, {self.state}>"

# Modelo para la tabla Puntos_Balance
class PuntosBalance(db.Model):
    __tablename__ = 'Puntos_Balance'  # Nombre de la tabla en la base de datos
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), primary_key=True)  # Clave primaria y foránea
    puntos_total = db.Column(db.Integer, nullable=False, default=0)  # Puntos disponibles
    redimidos_total = db.Column(db.Integer, nullable=False, default=0)  # Puntos redimidos
    actualizado_en = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # Última actualización

    def __repr__(self):
        return f"<PuntosBalance Usuario {self.id_usuario}, Puntos {self.puntos_total}>"

# Modelo para la tabla Menu_Objetos
class MenuObjetos(db.Model):
    __tablename__ = 'Menu_Objetos'  # Nombre de la tabla en la base de datos
    
    id_objeto = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre_objeto = db.Column(db.String(100), nullable=False, unique=True)  # Nombre del objeto (único)
    precio = db.Column(db.Numeric(10, 2), nullable=True)  # Precio del objeto
    categoria = db.Column(db.String(45), nullable=False)  # Categoría del objeto
    calorias = db.Column(db.Integer, nullable=True)  # Calorías del objeto
    imagen_url = db.Column(db.String(255), nullable=True)  # URL de la imagen del objeto

    def __repr__(self):
        return f"<MenuObjetos {self.nombre_objeto} - {self.categoria}>"

# Modelo para la tabla Orden
class Orden(db.Model):
    __tablename__ = 'Orden'  # Nombre de la tabla en la base de datos

    id_transaccion = db.Column(db.Integer, primary_key=True)  # Clave primaria
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)  # Clave foránea a Usuarios
    id_delivery_address = db.Column(db.Integer, db.ForeignKey('Address.id_address'), nullable=False)  # Clave foránea a Address
    precio_total = db.Column(db.Numeric(10, 2), nullable=True)  # Precio total de la orden
    puntos_gastados = db.Column(db.Integer, nullable=True, default=0)  # Puntos redimidos
    puntos_ganados = db.Column(db.Integer, nullable=True, default=0)  # Puntos ganados
    fecha_orden = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Fecha de la orden

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