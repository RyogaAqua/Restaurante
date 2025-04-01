# filepath: c:\Users\emman\Documents\Restaurante\Logica\app\main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from .extensions import db  # Updated to use extensions.py
from .routes import auth_routes, menu_routes, order_routes, reward_routes, payment_routes
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register blueprints
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