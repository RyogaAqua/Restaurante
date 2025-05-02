import pytest
from flask import Flask
from ..app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

def test_register_endpoint(client):
    """
    Test to verify the /auth/register endpoint.
    """
    # Sample payload for registration
    payload = {
        "nombre_usuario": "Test",
        "apellido_usuario": "User",
        "email": "testuser@example.com",
        "telefono": "1234567890",
        "contrasena": "password123",
        "metodo_pago": "credit_card",
        "address": {
            "address": "123 Test St",
            "zip_code": "12345",
            "state": "Test State",
            "country": "Test Country",
            "city": "Test City"
        }
    }

    # Send POST request to /auth/register
    response = client.post('/auth/register', json=payload)

    # Assert the response status code and message
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json.get("message") == "User registered successfully", f"Unexpected response message: {response.json}"