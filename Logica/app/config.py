import os

# Clase base de configuración con valores predeterminados.
class Config:
    # Cambia la URI para que apunte a la base de datos 'mydb'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:2016@127.0.0.1/mydb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

# Configuración específica para el entorno de desarrollo.
class DevelopmentConfig(Config):
    DEBUG = True  # Activa el modo de depuración.
    SQLALCHEMY_ECHO = True  # Registra las consultas SQL para depuración.

# Configuración específica para el entorno de pruebas.
class TestingConfig(Config):
    TESTING = True  # Activa el modo de pruebas.
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')  # Base de datos en memoria para pruebas.

# Configuración específica para el entorno de producción.
class ProductionConfig(Config):
    DEBUG = False  # Desactiva el modo de depuración.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Asegúrate de configurar esta variable en producción.

# Diccionario para mapear nombres de entornos a clases de configuración.
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}