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

# 3. CLASE ABSTRACTA BASE (Abstracción)

class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general del sistema Software FJ.
    Establece un contrato para la representación en texto y validación de datos.
    """
    
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad  # Encapsulación de ID

    @property
    def id_entidad(self) -> str:
        """Getter encapsulado para el ID de la entidad."""
        return self._id_entidad

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que obliga a las clases hijas a implementar sus propias reglas de validación."""
        pass

    @abstractmethod
    def obtener_informacion(self) -> dict:
        """Método abstracto para retornar un diccionario con los datos de la entidad."""
        pass

# 4. CLASE CLIENTE (Encapsulación y Validaciones)

class Cliente(EntidadBase):
    """
    Representa a un cliente de Software FJ con validaciones rigurosas y encapsulación estricta.
    """
    
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        # Asignación mediante setters para aplicar validaciones desde la instanciación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value or not isinstance(value, str) or len(value.strip()) < 3:
            raise ErrorCliente(f"Nombre de cliente inválido: '{value}'. Debe tener al menos 3 caracteres.")
        self._nombre = value.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, value: str):
        if not value or "@" not in value or "." not in value:
            raise ErrorCliente(f"Correo electrónico inválido: '{value}'. Formato requerido: user@domain.com")
        self._correo = value.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str):
        if not value or not value.isdigit() or len(value) < 7:
            raise ErrorCliente(f"Teléfono inválido: '{value}'. Debe contener solo dígitos y al menos 7 caracteres.")
        self._telefono = value.strip()

    def validar(self) -> bool:
        """Valida que los datos del cliente cumplan con los criterios internos."""
        try:
            if self._nombre and self._correo and self._telefono:
                return True
            return False
        except Exception as e:
            raise ErrorCliente("Error interno al validar el cliente.") from e

    def obtener_informacion(self) -> dict:
        return {
            "tipo": "Cliente",
            "id": self.id_entidad,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono
        }

# 5. CLASE ABSTRACTA SERVICIO Y POLIMORFISMO

class Servicio(ABC):
    """
    Clase abstracta que define la estructura común para los servicios ofrecidos por Software FJ.
    Implementa polimorfismo mediante métodos abstractos sobrescritos por las subclases.
    """
    
    def __init__(self, codigo: str, nombre_servicio: str, tarifa_base: float):
        self._codigo = codigo
        self._nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base  # Usa propiedad setter

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, value: float):
        if value < 0:
            raise ErrorServicio(f"La tarifa base no puede ser negativa: {value}")
        self._tarifa_base = float(value)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método polimórfico abstracto para calcular costos según las reglas de cada servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto para obtener la descripción detallada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, *args, **kwargs) -> bool:
        """Valida los parámetros específicos de cada tipo de servicio."""
        pass

# 6. CLASES DERIVADAS DE SERVICIOS (Herencia)

class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas físicas o virtuales para reuniones."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, nombre, tarifa_base)
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacity(self, value: int): # Nota: propiedad interna controlada
        pass

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, value: int):
        if value <= 0:
            raise ErrorServicio("La capacidad de la sala debe ser mayor a 0.")
        self._capacidad = int(value)

    def validar_parametros(self, horas: int = 0, *args, **kwargs) -> bool:
        if horas <= 0:
            raise ErrorServicio(f"Cantidad de horas inválida ({horas}) para reserva de sala.")
        return True

    def calcular_costo(self, horas: int = 1, incluir_proyector: bool = False, descuento_porcentaje: float = 0.0) -> float:
        """
        Método sobrecargado mediante argumentos opcionales y predeterminados.
        Calcula el costo considerando horas, cargos adicionales por proyector y descuentos.
        """
        self.validar_parametros(horas=horas)
        costo = self.tarifa_base * horas
        if incluir_proyector:
            costo += 50.0  # Cargo fijo por proyector
        if descuento_porcentaje > 0:
            costo -= costo * (descuento_porcentaje / 100.0)
        return round(costo, 2)

    def describir_servicio(self) -> str:
        return f"Reserva de Sala: '{self.nombre_servicio}' (Capacidad: {self.capacidad} personas, Tarifa base: ${self.tarifa_base}/hr)"

class AlquilerEquipos(Servicio):
    """Servicio especializado 2: Alquiler temporal de equipos tecnológicos."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, dias: int = 0, *args, **kwargs) -> bool:
        if dias <= 0:
            raise ErrorServicio(f"Cantidad de días inválida ({dias}) para alquiler de equipos.")
        return True

    def calcular_costo(self, dias: int = 1, seguro_inluido: bool = False) -> float:
        """Calcula el costo por días de alquiler, sumando seguro opcional si se requiere."""
        self.validar_parametros(dias=dias)
        costo = self.tarifa_base * dias
        if seguro_inluido:
            costo += 30.0 * dias  # Costo diario de seguro
        return round(costo, 2)

    def describir_servicio(self) -> str:
        return f"Alquiler de Equipo: '{self.nombre_servicio}' [Tipo: {self.tipo_equipo}, Tarifa base: ${self.tarifa_base}/día]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Asesorías técnicas o de arquitectura de software especializadas."""
    
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, nivel_experto: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.nivel_experto = nivel_experto

    def validar_parametros(self, sesiones: int = 0, *args, **kwargs) -> bool:
        if sesiones <= 0:
            raise ErrorServicio(f"Número de sesiones inválido ({sesiones}) para asesoría especializada.")
        return True

    def calcular_costo(self, sesiones: int = 1, impuestos: float = 19.0) -> float:
        """Calcula el costo de las asesorías aplicando impuestos configurables."""
        self.validar_parametros(sesiones= sesiones if 'sesions' in locals() else sesiones)
        costo_base = self.tarifa_base * sesiones
        costo_total = costo_base + (costo_base * (impuestos / 100.0))
        return round(costo_total, 2)

    def describir_servicio(self) -> str:
        return f"Asesoría Especializada: '{self.nombre_servicio}' (Nivel: {self.nivel_experto}, Tarifa base: ${self.tarifa_base}/sesión)"
