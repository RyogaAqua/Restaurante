"""
Este módulo inicializa los servicios disponibles en la aplicación.

Los servicios son responsables de manejar la lógica de negocio específica
de diferentes áreas funcionales, como autenticación, pedidos, recompensas y pagos.
"""

from .auth_service import AuthService  # Cambiar a import relativo
from .order_service import OrderService  # Cambiar a import relativo
from .reward_service import RewardService  # Cambiar a import relativo
from .payment_service import PaymentService  # Cambiar a import relativo
