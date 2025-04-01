import logging
from ..models import Usuario  # Corrected import to use the correct class name
from app.extensions import db  # Import db from extensions.py

class RewardService:

    def __init__(self):
        # Define rewards (consider moving this to a database for scalability)
        self.rewards = {
            "free_burger": 100,  # Requires 100 points for a free burger
            "free_fries": 50,    # Requires 50 points for free fries
        }

    def get_available_rewards(self, user_id):
        """
        Retrieve available rewards for a user based on their points.
        :param user_id: ID of the user.
        :return: List of available rewards.
        """
        try:
            user = Usuario.query.get(user_id)  # Updated to use the correct class name
            if not user:
                raise ValueError("User not found.")

            user_points = user.puntos  # Updated to match the field name in the Usuario model
            available_rewards = []

            # Check which rewards are available based on user points
            for reward, required_points in self.rewards.items():
                if user_points >= required_points:
                    available_rewards.append({
                        "reward": reward,
                        "required_points": required_points
                    })

            return available_rewards
        except Exception as e:
            logging.error(f"Error retrieving rewards for user {user_id}: {e}")
            raise ValueError("An error occurred while retrieving rewards.")

    def redeem_reward(self, user_id, reward_name):
        """
        Allow a user to redeem a reward using their points.
        :param user_id: ID of the user.
        :param reward_name: Name of the reward to redeem.
        :return: Result of the reward redemption.
        """
        try:
            user = Usuario.query.get(user_id)  # Updated to use the correct class name
            if not user:
                raise ValueError("User not found.")

            user_points = user.puntos  # Updated to match the field name in the Usuario model

            # Check if the reward exists
            if reward_name not in self.rewards:
                raise ValueError("Invalid reward.")

            required_points = self.rewards[reward_name]

            # Check if the user has enough points
            if user_points < required_points:
                raise ValueError("Insufficient points to redeem this reward.")

            # Deduct points and update the user's record
            user.puntos -= required_points  # Updated to match the field name in the Usuario model
            db.session.commit()

            return {"message": f"Reward '{reward_name}' redeemed successfully."}
        except Exception as e:
            logging.error(f"Error redeeming reward '{reward_name}' for user {user_id}: {e}")
            raise ValueError("An error occurred while redeeming the reward.")

    def get_user_points(self, user_id):
        """
        Retrieve the current points of a user.
        :param user_id: ID of the user.
        :return: User's points.
        """
        try:
            user = Usuario.query.get(user_id)  # Updated to use the correct class name
            if not user:
                raise ValueError("User not found.")
            
            return user.puntos  # Updated to match the field name in the Usuario model
        except Exception as e:
            logging.error(f"Error retrieving points for user {user_id}: {e}")
            raise ValueError("An error occurred while retrieving user points.")

    def update_user_points(self, user_id, points):
        """
        Update a user's points (add or subtract).
        :param user_id: ID of the user.
        :param points: Points to add or subtract.
        :return: Updated total points of the user.
        """
        try:
            user = Usuario.query.get(user_id)  # Updated to use the correct class name
            if not user:
                raise ValueError("User not found.")
            
            user.puntos += points  # Updated to match the field name in the Usuario model
            db.session.commit()

            return user.puntos  # Updated to match the field name in the Usuario model
        except Exception as e:
            logging.error(f"Error updating points for user {user_id}: {e}")
            raise ValueError("An error occurred while updating user points.")