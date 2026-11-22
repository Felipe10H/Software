from entidades import Entidad
from excepciones import DatoInvalidoError


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = self._validar_texto(nombre, "nombre")
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError(f"El {campo} no puede estar vacío.")
        return valor.strip()

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        telefono = str(telefono).strip()
        digitos = "".join(c for c in telefono if c.isdigit())
        if len(digitos) < 7:
            raise DatoInvalidoError("El teléfono debe contener al menos 7 dígitos.")
        return telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return f"Cliente {self.identificador}: {self.nombre} | {self.correo} | {self.telefono}"

    def __str__(self):
        return self.describir()
