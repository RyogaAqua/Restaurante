import os
from .database import init_app, db  # Cambiar a usar database.py para la configuración de la base de datos

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:2016@localhost/restaurantewk')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración específica para el entorno de desarrollo.
class DevelopmentConfig(Config):
    DEBUG = True  # Activa el modo de depuración.

# Configuración específica para el entorno de pruebas.
class TestingConfig(Config):
    TESTING = True  # Activa el modo de pruebas.

# Configuración específica para el entorno de producción.
class ProductionConfig(Config):
    DEBUG = False  # Desactiva el modo de depuración.

# Diccionario para mapear nombres de entornos a clases de configuración.
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}