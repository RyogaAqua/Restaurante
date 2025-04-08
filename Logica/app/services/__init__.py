"""
Este módulo inicializa los servicios disponibles en la aplicación.

Los servicios son responsables de manejar la lógica de negocio específica
de diferentes áreas funcionales, como autenticación, pedidos, recompensas y pagos.
"""

from .auth_service import AuthService  # Servicio para manejar la autenticación de usuarios
from .order_service import OrderService  # Servicio para manejar la lógica de los pedidos
from .reward_service import RewardService  # Servicio para manejar el sistema de recompensas
from .payment_service import PaymentService  # Servicio para manejar los pagos
