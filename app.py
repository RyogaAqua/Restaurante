from flask import Flask
from flask_migrate import Migrate
from Logica.app.database import db, init_app

app = Flask(__name__)

# Inicializa la base de datos
init_app(app)

# Configura Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
