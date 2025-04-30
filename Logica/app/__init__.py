import os
from flask import Flask, send_from_directory

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.

    - Configura la aplicación utilizando la clase Config.
    - Registra los blueprints para manejar las rutas.

    Returns:
        app (Flask): La instancia de la aplicación Flask configurada.
    """
    # Configura Flask para usar PaginaWeb2 como base para plantillas y archivos estáticos
    app = Flask(
        __name__,
        static_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2'),
        template_folder=os.path.join('..', '..', 'Pagina_Web', 'PaginaWeb2')
    )

    # Ruta para la página principal
    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    # Ruta para servir otros archivos HTML
    @app.route('/<path:filename>')
    def serve_html(filename):
        return app.send_static_file(filename)

    return app

