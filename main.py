from flask import Flask
from flask_migrate import Migrate
from Logica.app.database import db, init_app
from Logica.app.main import create_app  # Importar la función create_app desde Logica.app.main

# Use the create_app function to initialize the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
