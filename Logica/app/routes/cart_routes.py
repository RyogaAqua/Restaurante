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
    response = []
    for item in cart_items:
        use_points = getattr(item.CartItem, 'Use_Points', False)
        # Siempre incluir ambos campos, aunque sean None
        response.append({
            'id': item.CartItem.Id_Cart,
            'name': item.MenuObjetos.Nombre_Objeto,
            'price': item.MenuObjetos.Precio if not use_points else None,
            'points': item.MenuObjetos.Precio_Puntos if use_points else None,
            'image_url': item.MenuObjetos.Imagen_URL,
            'quantity': item.CartItem.Cantidad
        })

    # Calcular el total en dinero y puntos (evita error de None)
    total = sum((item['price'] or 0) * item['quantity'] for item in response)
    total_points = sum((item['points'] or 0) * item['quantity'] for item in response)
    puntos = int(total * 0.10)

    logger.debug(f"Datos enviados al frontend: {response}, total: {total}, puntos: {puntos}, total_points: {total_points}")
    return jsonify({'items': response, 'total': total, 'puntos': puntos, 'total_points': total_points})

@bp.route('', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    id_objeto = data.get('id_objeto')
    quantity = data.get('quantity', 1)
    use_points = data.get('use_points', False)

    if not id_objeto:
        logger.debug("Faltan campos requeridos: id_objeto")
        return jsonify({'error': 'Faltan campos requeridos: id_objeto'}), 400

    try:
        logger.debug(f"Intentando agregar al carrito: id_objeto={id_objeto}, quantity={quantity}, use_points={use_points}")
        cart_item = CartItem.query.filter_by(Id_Usuario=current_user.Id_Usuario, Id_Objeto=id_objeto, Use_Points=use_points).first()
        if cart_item:
            cart_item.Cantidad += quantity
            logger.debug(f"Actualizando cantidad del item {id_objeto} a {cart_item.Cantidad}")
        else:
            cart_item = CartItem(Id_Usuario=current_user.Id_Usuario, Id_Objeto=id_objeto, Cantidad=quantity, Use_Points=use_points)
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

@bp.route('/checkout', methods=['POST'])
def checkout_cart():
    """Procesar el pago del carrito, guardar la orden y sumar puntos al usuario."""
    from Logica.app.models import CartItem, db, MenuObjetos, PuntosBalance
    from flask_login import current_user
    import datetime

    cart_items = db.session.query(CartItem).filter_by(Id_Usuario=current_user.Id_Usuario).all()
    if not cart_items:
        return jsonify({'message': 'El carrito está vacío.'}), 400

    total = 0
    for item in cart_items:
        menu_obj = db.session.query(MenuObjetos).filter_by(Id_Objeto=item.Id_Objeto).first()
        if menu_obj:
            total += item.Cantidad * float(menu_obj.Precio)

    # Calcular puntos ganados (10% del total)
    puntos_ganados = int(total * 0.10)

    # Sumar puntos al usuario en puntos_balance
    puntos_row = db.session.query(PuntosBalance).filter_by(Id_Usuario=current_user.Id_Usuario).first()
    if puntos_row:
        puntos_row.Puntos_Total += puntos_ganados
        puntos_row.Actualizado_En = datetime.datetime.now()
    else:
        puntos_row = PuntosBalance(
            Id_Usuario=current_user.Id_Usuario,
            Puntos_Total=puntos_ganados,
            Redimidos_Total=0,
            Actualizado_En=datetime.datetime.now()
        )
        db.session.add(puntos_row)
    db.session.commit()

    # Limpiar el carrito
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify({'message': f'¡Pago procesado exitosamente! Has ganado {puntos_ganados} puntos.'})
