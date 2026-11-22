from abc import abstractmethod
from entidades import Entidad
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser un número mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa = float(tarifa)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Parámetros opcionales: permite calcular con o sin impuesto/descuento."""
        self.validar_parametros(duracion)
        for valor, etiqueta in ((impuesto, "impuesto"), (descuento, "descuento")):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 100:
                raise DatoInvalidoError(f"El {etiqueta} debe estar entre 0 y 100.")
        subtotal = self.tarifa * duracion
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)
        return round(total, 2)

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad < 1:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        self.validar_disponibilidad()
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración de la sala debe ser mayor que cero.")

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad: {self.capacidad}) - ${self.tarifa:.2f} por hora"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades < 1:
            raise DatoInvalidoError("Las unidades de equipo deben ser un entero positivo.")
        self.unidades = unidades

    def validar_parametros(self, duracion):
        self.validar_disponibilidad()
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración del alquiler debe ser mayor que cero.")

    def describir(self):
        return f"Equipo '{self.nombre}' ({self.unidades} unidades) - ${self.tarifa:.2f} por hora"


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre, tarifa, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("La especialidad no puede estar vacía.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion):
        self.validar_disponibilidad()
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser mayor que cero.")

    def describir(self):
        return f"Asesoría de {self.especialidad} - ${self.tarifa:.2f} por hora"
