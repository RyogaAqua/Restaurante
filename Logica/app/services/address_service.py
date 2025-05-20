from ..models import Address, Usuarios  # Import relativo
from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar las direcciones de los usuarios,
incluyendo agregar, listar y eliminar direcciones.
"""

class AddressService:
    """
    Servicio para manejar la lógica relacionada con las direcciones.
    """

    def add_address(self, user_id, address_data):
        """
        Agrega una nueva dirección para un usuario.

        Args:
            user_id (int): ID del usuario.
            address_data (dict): Diccionario con los detalles de la dirección.

        Returns:
            dict: La dirección recién agregada en formato de diccionario.

        Raises:
            ValueError: Si ocurre un error al agregar la dirección.
        """
        try:
            # Crear la nueva dirección
            new_address = Address(
                address=address_data.get('address'),
                city=address_data.get('city'),
                state=address_data.get('state'),
                zip_code=address_data.get('zip_code'),
                country=address_data.get('country')
            )
            db.session.add(new_address)
            db.session.flush()  # Asegura que la dirección tenga un ID antes de usarla

            # Asociar la dirección al usuario
            user = Usuarios.query.get(user_id)
            if not user:
                raise ValueError("Usuario no encontrado.")
            user.id_address = new_address.id_address

            db.session.commit()
            return new_address.to_dict()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al agregar la dirección: {e}")

    def list_addresses(self, user_id):
        """
        Lista todas las direcciones de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de direcciones en formato de diccionario.

        Raises:
            ValueError: Si ocurre un error al listar las direcciones.
        """
        try:
            user = Usuarios.query.get(user_id)
            if not user:
                raise ValueError("Usuario no encontrado.")

            addresses = Address.query.filter_by(id_address=user.id_address).all()
            return [address.to_dict() for address in addresses]
        except Exception as e:
            raise ValueError(f"Error al listar las direcciones: {e}")

    def delete_address(self, address_id):
        """
        Elimina una dirección de la base de datos.

        Args:
            address_id (int): ID de la dirección a eliminar.

        Raises:
            ValueError: Si ocurre un error al eliminar la dirección.
        """
        try:
            address = Address.query.get(address_id)
            if not address:
                raise ValueError("Dirección no encontrada.")

            db.session.delete(address)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al eliminar la dirección: {e}")
