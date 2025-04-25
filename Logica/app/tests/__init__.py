"""
Este módulo inicializa el paquete de pruebas para la aplicación Flask.

El paquete `tests` contiene los archivos necesarios para realizar pruebas
unitarias y funcionales de la aplicación.
"""

import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    """
    Crea una instancia de la aplicación Flask configurada para pruebas.

    Returns:
        Flask: La instancia de la aplicación Flask.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base de datos en memoria para pruebas
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos de prueba
        yield app
        db.session.remove()
        db.drop_all()  # Elimina las tablas después de las pruebas

@pytest.fixture
def client(app):
    """
    Proporciona un cliente de prueba para realizar solicitudes a la aplicación.

    Args:
        app (Flask): La instancia de la aplicación Flask.

    Returns:
        FlaskClient: El cliente de prueba.
    """
    return app.test_client()
