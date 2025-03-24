from app.models import Usuarios, Puntos
from app.config import db

class RewardService:

    def __init__(self):
        # Aquí se pueden agregar configuraciones si es necesario (por ejemplo, ofertas, descuentos, etc.)
        self.rewards = {
            "free_burger": 100,  # Requiere 100 puntos para obtener una hamburguesa gratis
            "free_fries": 50,    # Requiere 50 puntos para obtener papas fritas gratis
        }

    def get_available_rewards(self, user_id):
        """
        Obtener las recompensas disponibles para un usuario.
        :param user_id: ID del usuario.
        :return: Diccionario con las recompensas disponibles.
        """
        user = Usuarios.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")

        user_points = user.Puntos
        available_rewards = []

        # Comprobar qué recompensas están disponibles según los puntos del usuario
        for reward, required_points in self.rewards.items():
            if user_points >= required_points:
                available_rewards.append({
                    "reward": reward,
                    "required_points": required_points
                })

        return available_rewards

    def redeem_reward(self, user_id, reward_name):
        """
        Permite a un usuario canjear una recompensa usando sus puntos.
        :param user_id: ID del usuario.
        :param reward_name: Nombre de la recompensa que desea canjear.
        :return: Resultado del canje de recompensa.
        """
        user = Usuarios.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")

        user_points = user.Puntos

        # Verificar si la recompensa existe
        if reward_name not in self.rewards:
            raise ValueError("Recompensa no válida.")

        required_points = self.rewards[reward_name]

        # Verificar si el usuario tiene suficientes puntos
        if user_points < required_points:
            raise ValueError("Puntos insuficientes para canjear esta recompensa.")

        # Deduct points and update the user's record
        user.Puntos -= required_points
        db.session.commit()

        # Return confirmation message
        return {"message": f"Recompensa '{reward_name}' canjeada exitosamente."}

    def get_user_points(self, user_id):
        """
        Obtener los puntos actuales de un usuario.
        :param user_id: ID del usuario.
        :return: Puntos del usuario.
        """
        user = Usuarios.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")
        
        return user.Puntos

    def update_user_points(self, user_id, points):
        """
        Actualizar los puntos de un usuario (agregar o restar).
        :param user_id: ID del usuario.
        :param points: Puntos a agregar o restar.
        :return: El total de puntos actualizados del usuario.
        """
        user = Usuarios.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")
        
        user.Puntos += points
        db.session.commit()

        return user.Puntos
