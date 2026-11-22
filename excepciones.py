class ErrorSoftwareFJ(Exception):
    """Excepción base personalizada del sistema."""


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando un dato no cumple las validaciones."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se usa cuando una operación no está permitida."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se usa cuando un servicio no está disponible."""


class ReservaError(ErrorSoftwareFJ):
    """Se usa cuando una reserva no puede procesarse."""
