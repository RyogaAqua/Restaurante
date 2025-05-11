from flask import Blueprint, jsonify
from Logica.app.models import MenuObjetos

"""
Este módulo define las rutas relacionadas con el menú, permitiendo a los usuarios
recuperar los elementos disponibles en el menú.
"""

# Crear un blueprint para las rutas del menú
menu_routes = Blueprint('menu_routes', __name__)

bp = Blueprint('menu', __name__)

@bp.route('/api/menu', methods=['GET'])
def get_menu():
    """
    Endpoint para obtener el menú desde la base de datos.
    """
    menu_items = MenuObjetos.query.all()
    menu = [
        {
            "id": item.Id_Objeto,
            "name": item.Nombre_Objeto,
            "price": item.Precio,
            "category": item.Categoria,
            "calories": item.Calorias,
            "image_url": item.Imagen_URL
        }
        for item in menu_items
    ]
    return jsonify(menu)