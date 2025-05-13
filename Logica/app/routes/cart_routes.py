from flask import Blueprint, request, jsonify, session
from flask_login import current_user
from Logica.app.models import CartItem, MenuObjetos, db
import logging

"""
Este módulo define las rutas relacionadas con el carrito, permitiendo a los usuarios
guardar y recuperar su carrito desde el backend.
"""

# Crear un blueprint para las rutas del carrito
bp = Blueprint('cart', __name__)

logger = logging.getLogger(__name__)

@bp.route('', methods=['GET'])
def get_cart():
    """Obtener los elementos del carrito del usuario autenticado."""
    # Verificar si el usuario está autenticado
    if not current_user.is_authenticated:
        logger.debug("Usuario no autenticado al intentar obtener el carrito.")
        return jsonify({'error': 'Usuario no autenticado'}), 401

    # Registrar el usuario actual para depuración
    logger.debug(f"Usuario autenticado: {current_user.Id_Usuario}")

    # Restaurar la funcionalidad del carrito para asegurar que los datos se envíen correctamente
    cart_items = db.session.query(CartItem, MenuObjetos).join(MenuObjetos, CartItem.Id_Objeto == MenuObjetos.Id_Objeto).filter(CartItem.Id_Usuario == current_user.Id_Usuario).all()

    # Construir la respuesta con los datos necesarios
    response = [{
        'id': item.CartItem.Id_Cart,
        'name': item.MenuObjetos.Nombre_Objeto,
        'price': item.MenuObjetos.Precio,
        'image_url': item.MenuObjetos.Imagen_URL,
        'quantity': item.CartItem.Cantidad
    } for item in cart_items]

    logger.debug(f"Datos enviados al frontend: {response}")
    return jsonify(response)

@bp.route('', methods=['POST'])
def add_to_cart():
    """Agregar un elemento al carrito del usuario autenticado."""
    data = request.get_json()
    id_objeto = data.get('id_objeto')
    quantity = data.get('quantity', 1)

    if not id_objeto:
        logger.debug("Faltan campos requeridos: id_objeto")
        return jsonify({'error': 'Faltan campos requeridos: id_objeto'}), 400

    try:
        logger.debug(f"Intentando agregar al carrito: id_objeto={id_objeto}, quantity={quantity}")
        cart_item = CartItem.query.filter_by(Id_Usuario=current_user.Id_Usuario, Id_Objeto=id_objeto).first()
        if cart_item:
            cart_item.Cantidad += quantity
            logger.debug(f"Actualizando cantidad del item {id_objeto} a {cart_item.Cantidad}")
        else:
            cart_item = CartItem(Id_Usuario=current_user.Id_Usuario, Id_Objeto=id_objeto, Cantidad=quantity)
            db.session.add(cart_item)
            logger.debug(f"Agregando nuevo item al carrito: {cart_item}")

        db.session.commit()
        logger.debug("Cambios confirmados en la base de datos.")
        return jsonify({'message': 'Item agregado al carrito'}), 201

    except Exception as e:
        logger.error(f"Error al agregar al carrito: {e}")
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/<int:item_id>', methods=['PATCH'])
def update_cart_item(item_id):
    """Actualizar la cantidad de un elemento en el carrito del usuario autenticado."""
    data = request.get_json()
    change = data.get('change')

    if change is None:
        return jsonify({'error': 'Falta el campo change'}), 400

    cart_item = CartItem.query.filter_by(Id_Usuario=current_user.Id_Usuario, Id_Cart=item_id).first()
    if not cart_item:
        return jsonify({'error': 'Elemento no encontrado en el carrito'}), 404

    # Depuración: registrar la solicitud de actualización
    logger.debug(f"Actualizando cantidad: item_id={item_id}, change={change}")

    if cart_item.Cantidad + change <= 0:
        logger.debug(f"Eliminando el elemento del carrito: item_id={item_id}")
        db.session.delete(cart_item)
    else:
        cart_item.Cantidad += change
        logger.debug(f"Nueva cantidad para item_id={item_id}: {cart_item.Cantidad}")
        db.session.add(cart_item)

    db.session.commit()
    logger.debug("Cambios confirmados en la base de datos.")

    return jsonify({'message': 'Cantidad actualizada correctamente'})

@bp.route('/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Eliminar un elemento del carrito del usuario autenticado."""
    cart_item = CartItem.query.filter_by(Id_Usuario=current_user.Id_Usuario, Id_Cart=item_id).first()
    if not cart_item:
        return jsonify({'error': 'Elemento no encontrado en el carrito'}), 404

    # Depuración: registrar la solicitud de eliminación
    logger.debug(f"Eliminando elemento del carrito: item_id={item_id}")

    db.session.delete(cart_item)
    db.session.commit()
    logger.debug("Elemento eliminado del carrito y cambios confirmados en la base de datos.")

    return jsonify({'message': 'Elemento eliminado del carrito'})
