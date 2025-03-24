from flask import Flask, jsonify
from app.database import db
from app.routes import auth_routes, menu_routes, order_routes, reward_routes, payment_routes
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_routes.bp)
app.register_blueprint(menu_routes.bp)
app.register_blueprint(order_routes.bp)
app.register_blueprint(reward_routes.bp)
app.register_blueprint(payment_routes.bp)

@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Attempt to execute a simple query
        db.session.execute('SELECT 1')
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\models.py
from app.database import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    Puntos = db.Column(db.Integer)

    # Add other fields and methods as needed
