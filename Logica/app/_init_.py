from flask import Flask
from flask_migrate import Migrate
from .extensions import db  # Assuming db is defined in extensions.py
from .config import Config
from .routes import bp as routes_bp  # Import the main blueprint for routes

# Create a Migrate instance
migrate = Migrate()

# Function to create and configure the Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Register blueprints
    app.register_blueprint(routes_bp)

    # Add global error handlers (optional)
    register_error_handlers(app)

    return app

# Optional: Global error handlers
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An internal error occurred"}, 500