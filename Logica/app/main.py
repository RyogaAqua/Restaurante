import sys
import os

# Agrega el directorio actual al sistema de rutas para permitir importaciones relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify  # Importa Flask para crear la aplicación y jsonify para respuestas JSON
from .extensions import db  # Importa la instancia de la base de datos desde extensions.py
from .routes import auth_routes, menu_routes, order_routes, reward_routes, payment_routes  # Importa los blueprints
from .config import Config  # Importa la configuración de la aplicación

# Crea una instancia de la aplicación Flask
app = Flask(__name__)
# Configura la aplicación usando la clase Config
app.config.from_object(Config)

# Inicializa la base de datos con la aplicación Flask
db.init_app(app)

# Registra los blueprints para organizar las rutas de la aplicación
app.register_blueprint(auth_routes.bp)  # Rutas relacionadas con autenticación
app.register_blueprint(menu_routes.bp)  # Rutas relacionadas con el menú
app.register_blueprint(order_routes.bp)  # Rutas relacionadas con pedidos
app.register_blueprint(reward_routes.bp)  # Rutas relacionadas con recompensas
app.register_blueprint(payment_routes.bp)  # Rutas relacionadas con pagos

# Define una ruta para verificar la conexión con la base de datos
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Intenta ejecutar una consulta simple para verificar la conexión
        db.session.execute('SELECT 1')
        return jsonify({"message": "Database connection successful"}), 200  # Respuesta exitosa
    except Exception as e:
        # Si ocurre un error, devuelve un mensaje de error
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    # Ejecuta la aplicación en modo de depuración
    app.run(debug=True)