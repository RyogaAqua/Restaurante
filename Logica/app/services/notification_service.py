from ..extensions import db  # Import relativo

"""
Este módulo contiene la lógica para manejar las notificaciones,
incluyendo el envío y la recuperación de notificaciones.
"""

class NotificationService:
    """
    Servicio para manejar la lógica relacionada con las notificaciones.
    """

    def send_notification(self, user_id, message, notification_type='info'):
        """
        Envía una notificación a un usuario.

        Args:
            user_id (int): ID del usuario.
            message (str): Mensaje de la notificación.
            notification_type (str): Tipo de notificación (info, success, error).

        Raises:
            ValueError: Si ocurre un error al enviar la notificación.
        """
        try:
            notification = Notification(
                user_id=user_id,
                message=message,
                type=notification_type
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al enviar la notificación: {e}")

    def get_notifications(self, user_id):
        """
        Recupera las notificaciones de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de notificaciones en formato de diccionario.

        Raises:
            ValueError: Si ocurre un error al recuperar las notificaciones.
        """
        try:
            notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
            return [notification.to_dict() for notification in notifications]
        except Exception as e:
            raise ValueError(f"Error al recuperar las notificaciones: {e}")
