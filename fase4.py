import logging
from abc import ABC, abstractmethod
from datetime import datetime


# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS

logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)
# 2. EXCEPCIONES PERSONALIZADAS Y ENCADENAMIENTO
class SoftwareFJError(Exception):
    """Excepción base personalizada para todos los errores del sistema Software FJ."""
    pass

class ErrorCliente(SoftwareFJError):
    """Excepción lanzada ante fallos en los datos o validaciones de clientes."""
    pass

class ErrorServicio(SoftwareFJError):
    """Excepción lanzada ante parámetros inválidos o fallos en los servicios."""
    pass

class ErrorReserva(SoftwareFJError):
    """Excepción lanzada ante conflictos en la creación, confirmación o cancelación de reservas."""
    pass

