from flask import Blueprint, jsonify
from flask_login import current_user
from Logica.app.models import MenuObjetos, PuntosBalance

bp = Blueprint('point_store', __name__)

@bp.route('/api/point_store', methods=['GET'])
def get_point_store():
    """
    Endpoint para obtener los productos que se pueden comprar por puntos (Precio_Puntos no es NULL)
    """
    items = MenuObjetos.query.filter(MenuObjetos.Precio_Puntos != None).all()
    productos = [
        {
            "id": item.Id_Objeto,
            "name": item.Nombre_Objeto,
            "points": item.Precio_Puntos,
            "category": (item.Categoria.lower() if item.Categoria.lower() != 'accesorios' else 'accessories'),
            "calories": item.Calorias,
            "image_url": item.Imagen_URL
        }
        for item in items
    ]
    return jsonify(productos)

@bp.route('/api/point_store/user_points', methods=['GET'])
def get_user_points():
    if not current_user.is_authenticated:
        return jsonify({'points': 0})
    puntos = PuntosBalance.query.filter_by(Id_Usuario=current_user.Id_Usuario).first()
    return jsonify({'points': puntos.Puntos_Total if puntos else 0})
