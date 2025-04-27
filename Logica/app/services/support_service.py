from ..models import SupportMessage  # Import relativo
from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar los mensajes de soporte,
incluyendo el envío y la recuperación de mensajes.
"""

class SupportService:
    """
    Servicio para manejar la lógica relacionada con el soporte.
    """

    def send_message(self, user_id, subject, message):
        """
        Envía un mensaje al equipo de soporte.

        Args:
            user_id (int): ID del usuario que envía el mensaje.
            subject (str): Asunto del mensaje.
            message (str): Contenido del mensaje.

        Raises:
            ValueError: Si ocurre un error al enviar el mensaje.
        """
        try:
            support_message = SupportMessage(
                user_id=user_id,
                subject=subject,
                message=message
            )
            db.session.add(support_message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al enviar el mensaje de soporte: {e}")

    def get_messages(self, user_id):
        """
        Recupera los mensajes de soporte de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de mensajes en formato de diccionario.

        Raises:
            ValueError: Si ocurre un error al recuperar los mensajes.
        """
        try:
            messages = SupportMessage.query.filter_by(user_id=user_id).order_by(SupportMessage.created_at.desc()).all()
            return [message.to_dict() for message in messages]
        except Exception as e:
            raise ValueError(f"Error al recuperar los mensajes de soporte: {e}")
