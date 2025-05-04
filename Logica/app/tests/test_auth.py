import pytest
from Logica.app import create_app
from Logica.app.database import db  # Usar database.py para la configuración de la base de datos
from Logica.app.models import Usuarios, Address, PuntosBalance

@pytest.fixture(scope="module")
def app():
    """
    Configura la aplicación Flask para las pruebas.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "mysql+mysqlconnector://root:2016@localhost/restaurantewk",  # Configuración de la base de datos para pruebas
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    # Verificar que la URI de la base de datos esté configurada
    assert app.config["SQLALCHEMY_DATABASE_URI"] is not None, "SQLALCHEMY_DATABASE_URI no está configurada."

    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos de prueba
        yield app
        db.session.remove()
        db.drop_all()  # Limpia las tablas después de las pruebas

@pytest.fixture
def client(app):
    """
    Configura un cliente de prueba para la aplicación Flask.
    """
    return app.test_client()

def test_db_connection():
    """
    Verifica que la conexión a la base de datos sea exitosa.
    """
    try:
        with db.engine.connect() as connection:
            assert connection is not None, "No se pudo conectar a la base de datos."
    except Exception as e:
        pytest.fail(f"Error al conectar con la base de datos: {e}")

def test_register_endpoint(client):
    """
    Test to verify the /auth/register endpoint.
    """
    # Sample payload for registration
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "password": "password123",
        "address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "zip_code": "12345",
        "country": "Test Country"
    }

    # Send POST request to /auth/register
    response = client.post('/auth/register', json=payload)

    # Assert the response status code and message
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json.get("message") == "User registered successfully", f"Unexpected response message: {response.json}"

def test_register_user(client):
    """
    Test para verificar el endpoint /auth/register.
    """
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "password": "securepassword",
        "address": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62704",
        "country": "USA"
    }

    response = client.post('/auth/register', json=payload)

    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json.get("message") == "User registered successfully"

    # Verificar que el usuario fue creado en la base de datos
    user = Usuarios.query.filter_by(Email="john.doe@example.com").first()
    assert user is not None
    assert user.Nombre_Usuario == "John"

    # Verificar que el balance de puntos fue creado
    puntos_balance = PuntosBalance.query.filter_by(Id_Usuario=user.Id_Usuario).first()
    assert puntos_balance is not None
    assert puntos_balance.Puntos_Total == 0