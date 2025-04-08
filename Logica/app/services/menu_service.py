from ..models import MenuObjetos  # Importación relativa para el modelo MenuObjetos
from app.extensions import db  # Importa db desde extensions.py

"""
Este módulo contiene funciones para manejar la lógica relacionada con el menú,
incluyendo la recuperación, adición, actualización y eliminación de elementos del menú.
"""

def get_menu():
    """
    Recupera todos los elementos del menú desde la base de datos.

    Returns:
        list: Lista de elementos del menú en formato de diccionario.
    """
    try:
        menu_items = MenuObjetos.query.all()
        return [item.to_dict() for item in menu_items]
    except Exception as e:
        raise ValueError(f"Error al recuperar el menú: {e}")

def get_menu_by_category(category):
    """
    Recupera los elementos del menú filtrados por categoría.

    Args:
        category (str): La categoría por la cual filtrar los elementos del menú.

    Returns:
        list: Lista de elementos del menú en la categoría especificada.
    """
    try:
        menu_items = MenuObjetos.query.filter_by(categoria=category).all()
        return [item.to_dict() for item in menu_items]
    except Exception as e:
        raise ValueError(f"Error al recuperar el menú por categoría '{category}': {e}")

def add_menu_item(data):
    """
    Agrega un nuevo elemento al menú en la base de datos.

    Args:
        data (dict): Diccionario que contiene los detalles del nuevo elemento del menú.

    Returns:
        dict: El elemento del menú recién agregado en formato de diccionario.
    """
    try:
        new_item = MenuObjetos(
            upc_objeto=data.get('upc_objeto'),
            nombre_objeto=data.get('nombre_objeto'),
            precio=data.get('precio'),
            categoria=data.get('categoria'),
            calorias=data.get('calorias')
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_dict()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al agregar un elemento al menú: {e}")

def update_menu_item(upc_objeto, data):
    """
    Actualiza un elemento existente del menú en la base de datos.

    Args:
        upc_objeto (str): El UPC del elemento del menú a actualizar.
        data (dict): Diccionario que contiene los detalles actualizados del elemento del menú.

    Returns:
        dict: El elemento del menú actualizado en formato de diccionario.
    """
    try:
        item = MenuObjetos.query.get(upc_objeto)
        if not item:
            raise ValueError("Elemento del menú no encontrado.")

        item.nombre_objeto = data.get('nombre_objeto', item.nombre_objeto)
        item.precio = data.get('precio', item.precio)
        item.categoria = data.get('categoria', item.categoria)
        item.calorias = data.get('calorias', item.calorias)

        db.session.commit()
        return item.to_dict()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al actualizar un elemento del menú: {e}")

def delete_menu_item(upc_objeto):
    """
    Elimina un elemento del menú de la base de datos.

    Args:
        upc_objeto (str): El UPC del elemento del menú a eliminar.

    Returns:
        dict: Mensaje de éxito indicando que el elemento fue eliminado.
    """
    try:
        item = MenuObjetos.query.get(upc_objeto)
        if not item:
            raise ValueError("Elemento del menú no encontrado.")

        db.session.delete(item)
        db.session.commit()
        return {"message": f"Elemento del menú con UPC {upc_objeto} eliminado exitosamente."}
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al eliminar un elemento del menú: {e}")