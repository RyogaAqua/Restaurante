import os
import sys
import pytest
from .. import create_app
from ..models import Usuarios, Address, PuntosBalance
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Logica.app.routes.auth_routes import auth_bp
from werkzeug.security import generate_password_hash
from Logica.app.extensions import db  # Use the single SQLAlchemy instance
import unittest
import uuid  # For generating unique test data
import logging  # For debugging purposes

# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

@pytest.fixture(scope="module")
def app():
    """
    Configures the Flask application for testing.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Configura un cliente de prueba para la aplicación Flask.
    """
    return app.test_client()

def test_db_connection(app):
    """
    Verifies that the database connection is successful.
    """
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                assert connection is not None, "Database connection failed."
        except Exception as e:
            pytest.fail(f"Database connection error: {e}")

def test_register_endpoint(client):
    """
    Test to verify the /auth/signup endpoint.
    """
    payload = {
        "nombre": "Test",
        "apellido": "User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "password": "password123",
        "address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "zip_code": "12345",
        "country": "Test Country"
    }

    response = client.post('/auth/signup', json=payload)

    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json.get("message") == "Usuario creado exitosamente", f"Unexpected response message: {response.json}"

def test_register_user(client):
    """
    Test para verificar el endpoint /auth/signup.
    """
    payload = {
        "nombre": "John",
        "apellido": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "password": "securepassword",
        "address": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62704",
        "country": "USA"
    }

    response = client.post('/auth/signup', json=payload)

    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json.get("message") == "Usuario creado exitosamente"

    # Verificar que el usuario fue creado en la base de datos
    user = Usuarios.query.filter_by(Email="john.doe@example.com").first()
    assert user is not None
    assert user.Nombre_Usuario == "John"

    # Verificar que el balance de puntos fue creado
    puntos_balance = PuntosBalance.query.filter_by(Id_Usuario=user.Id_Usuario).first()
    assert puntos_balance is not None
    assert puntos_balance.Puntos_Total == 0

class TestSignIn(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        })

        with self.app.app_context():
            db.drop_all()  # Clear the database before each test
            db.create_all()  # Use the single instance for database setup

        self.client = self.app.test_client()

        hashed_password = generate_password_hash('testpassword')
        unique_email = f"testuser_{uuid.uuid4()}@example.com"  # Generate a unique email
        test_user = Usuarios(
            Nombre_Usuario='TestUser',  # Ensure this field is populated
            Apellido_Usuario='User',
            Email=unique_email,
            Hash_Contrasena_Usuario=hashed_password
        )
        with self.app.app_context():
            try:
                db.session.add(test_user)
                db.session.commit()
            except Exception as e:
                logging.error(f"Error during setup: {e}")
                db.session.rollback()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sign_in_success(self):
        with self.app.app_context():
            user = Usuarios.query.first()
            self.assertIsNotNone(user, "Test user was not created in the database.")

        response = self.client.post('/auth/signin', json={
            'email': user.Email,  # Use the email from the database
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Inicio de sesión exitoso', response.get_json().get('message', ''))

    def test_sign_in_invalid_password(self):
        response = self.client.post('/auth/signin', json={
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Credenciales inválidas', response.get_json().get('error', ''))

    def test_sign_in_user_not_found(self):
        response = self.client.post('/auth/signin', json={
            'email': 'nonexistent@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Credenciales inválidas', response.get_json().get('error', ''))

if __name__ == '__main__':
    unittest.main()