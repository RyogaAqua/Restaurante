import logging
from ..models import PuntosBalance  # Actualizado para usar la tabla Puntos_Balance
from app.extensions import db  # Importa db desde extensions.py

"""
Este módulo contiene la lógica para manejar el sistema de recompensas,
incluyendo la obtención de recompensas disponibles, el canje de recompensas
y la actualización de puntos de usuario.
"""

class RewardService:
    """
    Servicio para manejar la lógica relacionada con el sistema de recompensas.
    """

    def __init__(self):
        """
        Inicializa el servicio de recompensas y define las recompensas disponibles.
        """
        # Definir recompensas (considerar mover esto a una base de datos para mayor escalabilidad)
        self.rewards = {
            "free_burger": 100,  # Requiere 100 puntos para una hamburguesa gratis
            "free_fries": 50,    # Requiere 50 puntos para papas fritas gratis
        }

    def get_available_rewards(self, user_id):
        """
        Recupera las recompensas disponibles para un usuario basado en sus puntos.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de recompensas disponibles con los puntos requeridos.

        Raises:
            ValueError: Si ocurre un error al recuperar las recompensas.
        """
        try:
            puntos_balance = PuntosBalance.query.get(user_id)  # Recupera el balance de puntos por ID de usuario
            if not puntos_balance:
                raise ValueError("Usuario no encontrado o sin balance de puntos.")

            user_points = puntos_balance.puntos_total  # Obtiene los puntos actuales del usuario
            available_rewards = []

            # Verifica qué recompensas están disponibles según los puntos del usuario
            for reward, required_points in self.rewards.items():
                if user_points >= required_points:
                    available_rewards.append({
                        "reward": reward,
                        "required_points": required_points
                    })

            return available_rewards
        except Exception as e:
            logging.error(f"Error al recuperar recompensas para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al recuperar las recompensas.")

    def redeem_reward(self, user_id, reward_name):
        """
        Permite a un usuario canjear una recompensa utilizando sus puntos.

        Args:
            user_id (int): ID del usuario.
            reward_name (str): Nombre de la recompensa a canjear.

        Returns:
            dict: Resultado del canje de la recompensa.

        Raises:
            ValueError: Si ocurre un error durante el canje de la recompensa.
        """
        try:
            puntos_balance = PuntosBalance.query.get(user_id)  # Recupera el balance de puntos por ID de usuario
            if not puntos_balance:
                raise ValueError("Usuario no encontrado o sin balance de puntos.")

            user_points = puntos_balance.puntos_total  # Obtiene los puntos actuales del usuario

            # Verifica si la recompensa existe
            if reward_name not in self.rewards:
                raise ValueError("Recompensa inválida.")

            required_points = self.rewards[reward_name]

            # Verifica si el usuario tiene suficientes puntos
            if user_points < required_points:
                raise ValueError("Puntos insuficientes para canjear esta recompensa.")

            # Deduce los puntos y actualiza el registro del usuario
            puntos_balance.puntos_total -= required_points
            puntos_balance.redimidos_total += required_points
            db.session.commit()

            return {"message": f"Recompensa '{reward_name}' canjeada exitosamente."}
        except Exception as e:
            logging.error(f"Error al canjear la recompensa '{reward_name}' para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al canjear la recompensa.")

    def get_user_points(self, user_id):
        """
        Recupera los puntos actuales de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            int: Puntos actuales del usuario.

        Raises:
            ValueError: Si ocurre un error al recuperar los puntos del usuario.
        """
        try:
            puntos_balance = PuntosBalance.query.get(user_id)  # Recupera el balance de puntos por ID de usuario
            if not puntos_balance:
                raise ValueError("Usuario no encontrado o sin balance de puntos.")
            
            return puntos_balance.puntos_total
        except Exception as e:
            logging.error(f"Error al recuperar los puntos para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al recuperar los puntos del usuario.")

    def update_user_points(self, user_id, points):
        """
        Actualiza los puntos de un usuario (agregar o restar).

        Args:
            user_id (int): ID del usuario.
            points (int): Puntos a agregar o restar.

        Returns:
            int: Total actualizado de puntos del usuario.

        Raises:
            ValueError: Si ocurre un error al actualizar los puntos del usuario.
        """
        try:
            puntos_balance = PuntosBalance.query.get(user_id)  # Recupera el balance de puntos por ID de usuario
            if not puntos_balance:
                raise ValueError("Usuario no encontrado o sin balance de puntos.")
            
            puntos_balance.puntos_total += points
            db.session.commit()

            return puntos_balance.puntos_total
        except Exception as e:
            logging.error(f"Error al actualizar los puntos para el usuario {user_id}: {e}")
            raise ValueError("Ocurrió un error al actualizar los puntos del usuario.")