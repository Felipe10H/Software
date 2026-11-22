from cliente import Cliente
from reserva import Reserva
from excepciones import DatoInvalidoError, OperacionNoPermitidaError
from registro import eventos, errores


class SistemaSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto recibido no es un cliente válido.")
        if any(c.identificador == cliente.identificador for c in self._clientes):
            raise OperacionNoPermitidaError("Ya existe un cliente con ese identificador.")
        self._clientes.append(cliente)
        eventos.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        from servicio import Servicio
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto recibido no es un servicio válido.")
        if any(s.identificador == servicio.identificador for s in self._servicios):
            raise OperacionNoPermitidaError("Ya existe un servicio con ese identificador.")
        self._servicios.append(servicio)
        eventos.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, identificador, cliente_id, servicio_id, duracion):
        cliente = next((c for c in self._clientes if c.identificador == str(cliente_id)), None)
        servicio = next((s for s in self._servicios if s.identificador == str(servicio_id)), None)
        if cliente is None:
            raise DatoInvalidoError(f"No existe el cliente {cliente_id}.")
        if servicio is None:
            raise DatoInvalidoError(f"No existe el servicio {servicio_id}.")
        if any(r.identificador == str(identificador) for r in self._reservas):
            raise OperacionNoPermitidaError("Ya existe una reserva con ese identificador.")
        reserva = Reserva(identificador, cliente, servicio, duracion)
        self._reservas.append(reserva)
        eventos.info("Reserva creada: %s", identificador)
        return reserva

    def buscar_cliente(self, identificador):
        return next((c for c in self._clientes if c.identificador == str(identificador)), None)

    def buscar_servicio(self, identificador):
        return next((s for s in self._servicios if s.identificador == str(identificador)), None)

    def buscar_reserva(self, identificador):
        return next((r for r in self._reservas if r.identificador == str(identificador)), None)

    def mostrar_resumen(self):
        print("\n--- CLIENTES ---")
        for cliente in self._clientes:
            print(cliente.describir())
        print("\n--- SERVICIOS ---")
        for servicio in self._servicios:
            print(servicio.describir())
        print("\n--- RESERVAS ---")
        for reserva in self._reservas:
            print(reserva.describir())
