from ..models import MenuObjetos  # Corrected to use a relative import
from app.extensions import db  # Corrected to import db from extensions.py

def get_menu():
    """
    Retrieve all menu items from the database.
    :return: List of menu items.
    """
    try:
        menu_items = MenuObjetos.query.all()
        return [item.to_dict() for item in menu_items]
    except Exception as e:
        raise ValueError(f"Error retrieving menu: {e}")

def get_menu_by_category(category):
    """
    Retrieve menu items filtered by category.
    :param category: The category to filter by.
    :return: List of menu items in the specified category.
    """
    try:
        menu_items = MenuObjetos.query.filter_by(categoria=category).all()
        return [item.to_dict() for item in menu_items]
    except Exception as e:
        raise ValueError(f"Error retrieving menu by category '{category}': {e}")

def add_menu_item(data):
    """
    Add a new menu item to the database.
    :param data: Dictionary containing menu item details.
    :return: The newly added menu item.
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
        raise ValueError(f"Error adding menu item: {e}")

def update_menu_item(upc_objeto, data):
    """
    Update an existing menu item in the database.
    :param upc_objeto: The UPC of the menu item to update.
    :param data: Dictionary containing updated menu item details.
    :return: The updated menu item.
    """
    try:
        item = MenuObjetos.query.get(upc_objeto)
        if not item:
            raise ValueError("Menu item not found.")

        item.nombre_objeto = data.get('nombre_objeto', item.nombre_objeto)
        item.precio = data.get('precio', item.precio)
        item.categoria = data.get('categoria', item.categoria)
        item.calorias = data.get('calorias', item.calorias)

        db.session.commit()
        return item.to_dict()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error updating menu item: {e}")

def delete_menu_item(upc_objeto):
    """
    Delete a menu item from the database.
    :param upc_objeto: The UPC of the menu item to delete.
    :return: Success message.
    """
    try:
        item = MenuObjetos.query.get(upc_objeto)
        if not item:
            raise ValueError("Menu item not found.")

        db.session.delete(item)
        db.session.commit()
        return {"message": f"Menu item with UPC {upc_objeto} deleted successfully."}
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error deleting menu item: {e}")