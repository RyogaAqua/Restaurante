from flask import Flask
from flask_migrate import Migrate
from Logica.app.database import db  # Import absoluto
from Logica.app.config import Config  # Import absoluto
from Logica.app.routes import bp as routes_bp  # Import absoluto
from . import create_app

app = create_app()

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)

# Registrar blueprints
app.register_blueprint(routes_bp)

# Ruta para verificar la conexión a la base de datos
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        db.session.execute('SELECT 1')  # Consulta simple para verificar la conexión
        return {"message": "Conexión exitosa a la base de datos"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Punto de entrada principal
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
