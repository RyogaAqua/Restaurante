from ..models import Orden, PuntosBalance  # Import relativo
from sqlalchemy.sql import func

"""
Este módulo contiene la lógica para manejar las estadísticas de los usuarios,
incluyendo el total gastado, puntos ganados, pedidos realizados, etc.
"""

class StatsService:
    """
    Servicio para manejar la lógica relacionada con las estadísticas.
    """

    def get_user_stats(self, user_id):
        """
        Recupera estadísticas personales de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            dict: Estadísticas del usuario, incluyendo total gastado, puntos ganados, etc.

        Raises:
            ValueError: Si ocurre un error al recuperar las estadísticas.
        """
        try:
            # Total gastado por el usuario
            total_spent = (
                Orden.query.with_entities(func.sum(Orden.precio_total))
                .filter_by(id_usuario=user_id, estado='Pagado')
                .scalar()
            ) or 0

            # Total de puntos ganados
            total_points_earned = (
                Orden.query.with_entities(func.sum(Orden.puntos_ganados))
                .filter_by(id_usuario=user_id, estado='Pagado')
                .scalar()
            ) or 0

            # Total de pedidos realizados
            total_orders = (
                Orden.query.filter_by(id_usuario=user_id, estado='Pagado').count()
            )

            # Puntos actuales del usuario
            puntos_balance = PuntosBalance.query.get(user_id)
            current_points = puntos_balance.puntos_total if puntos_balance else 0

            return {
                "total_spent": float(total_spent),
                "total_points_earned": total_points_earned,
                "total_orders": total_orders,
                "current_points": current_points,
            }
        except Exception as e:
            raise ValueError(f"Error al recuperar las estadísticas del usuario: {e}")
