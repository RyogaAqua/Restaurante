import unittest
from flask import json
from Logica.app import create_app, db
from app.models import Usuarios, CartItem

class TestCart(unittest.TestCase):

    def setUp(self):
        """Configurar el entorno de prueba."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()  # Activar el contexto de la aplicación
        self.client = self.app.test_client()

        # Forzar la inicialización de db en las pruebas
        with self.app_context:  # Asegurar que las operaciones estén dentro del contexto
            db.session.remove()
            db.create_all()  # Crear las tablas en la base de datos de prueba

        print("Tablas creadas correctamente en la base de datos.")
        print("Contexto de la aplicación activado y base de datos inicializada correctamente.")

    def tearDown(self):
        """Limpiar el entorno de prueba."""
        with self.app_context:  # Asegurar que las operaciones estén dentro del contexto
            db.session.remove()
            db.drop_all()  # Eliminar las tablas de la base de datos de prueba
        self.app_context.pop()  # Desactivar el contexto de la aplicación

    def test_add_to_cart_with_login(self):
        """Agregar un artículo al carrito después de iniciar sesión."""
        with self.client.session_transaction() as session:
            session['user_id'] = 3

        response = self.client.post('/api/cart', json={"id_objeto": 1, "quantity": 2})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Item agregado al carrito", response.get_data(as_text=True))

        # Verificar que el artículo se haya agregado a la base de datos
        with self.app_context:  # Asegurar que la consulta esté dentro del contexto
            cart_item = CartItem.query.filter_by(user_id=3, id_objeto=1).first()
            self.assertIsNotNone(cart_item)
            self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_without_login(self):
        """Intentar agregar al carrito sin iniciar sesión."""
        # Asegurar que no hay usuario autenticado
        with self.client.session_transaction() as session:
            session.clear()

        response = self.client.post('/api/cart', json={"id_objeto": 1, "quantity": 2})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Debe iniciar sesión", response.get_data(as_text=True))

    def test_add_to_cart_with_invalid_data(self):
        """Intentar agregar al carrito con datos inválidos."""
        with self.client.session_transaction() as session:
            session['user_id'] = 3

        response = self.client.post('/api/cart', json={"quantity": 2})  # Actualizar prefijo
        self.assertEqual(response.status_code, 400)
        self.assertIn("Faltan campos requeridos", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
