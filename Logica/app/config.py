import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Clase base de configuración con valores predeterminados.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../instance/restaurante.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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