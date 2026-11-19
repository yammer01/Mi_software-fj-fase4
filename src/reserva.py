# src/reserva.py
# Importamos datetime para registrar la fecha y hora de creación de cada reserva.
from datetime import datetime
# Importamos las clases Cliente y Servicio desde src/modelos.py.
from src.modelos import Cliente, Servicio
# Importamos las excepciones personalizadas desde src/excepciones.py.
from src.excepciones import ReservaInvalidaError, ServicioNoDisponibleError, ServicioInvalidoError


# Clase que representa una reserva realizada por un cliente sobre un servicio.
class Reserva:
    # Estados válidos para el ciclo de vida de una reserva.
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    # Constructor de Reserva que vincula un cliente, un servicio y la cantidad/duración solicitada.
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, cantidad: float, descuento_pct: float = 0.0, porcentaje_impuesto: float = 0.0):
        # Validamos que el ID de la reserva sea un texto no vacío.
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            # Lanzamos ReservaInvalidaError si el identificador es inválido.
            raise ReservaInvalidaError("El ID de la reserva debe ser un texto no vacío.")
        # Validamos que el objeto recibido sea una instancia de Cliente.
        if not isinstance(cliente, Cliente):
            # Lanzamos ReservaInvalidaError si no se proporciona un Cliente válido.
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")
        # Validamos que el objeto recibido sea una instancia de Servicio.
        if not isinstance(servicio, Servicio):
            # Lanzamos ReservaInvalidaError si no se proporciona un Servicio válido.
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")
        # Validamos que el servicio esté disponible antes de crear la reserva.
        if not servicio.disponible:
            # Lanzamos ServicioNoDisponibleError si el servicio no está disponible.
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible para reservar.")
        # Validamos la cantidad o duración usando el método polimórfico del servicio.
        servicio.parametros_validacion(cantidad)
        # Guardamos el ID limpio de la reserva.
        self._id_reserva = id_reserva.strip()
        # Guardamos la referencia al cliente.
        self._cliente = cliente
        # Guardamos la referencia al servicio.
        self._servicio = servicio
        # Convertimos y guardamos la cantidad solicitada como flotante.
        self._cantidad = float(cantidad)
        # Guardamos el porcentaje de descuento opcional.
        self._descuento_pct = float(descuento_pct)
        # Guardamos el porcentaje de impuesto opcional.
        self._porcentaje_impuesto = float(porcentaje_impuesto)
        # Inicializamos el estado de la reserva en PENDIENTE.
        self._estado = "PENDIENTE"
        # Registramos la marca de tiempo de creación de la reserva.
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Calculamos y almacenamos el costo total de la reserva.
        self._costo_total = self.calcular_costo()

    # Propiedad de solo lectura para obtener el ID de la reserva.
    @property
    def id_reserva(self) -> str:
        # Retornamos el ID encapsulado.
        return self._id_reserva

    # Propiedad de solo lectura para obtener el cliente asociado.
    @property
    def cliente(self) -> Cliente:
        # Retornamos el objeto Cliente.
        return self._cliente

    # Propiedad de solo lectura para obtener el servicio asociado.
    @property
    def servicio(self) -> Servicio:
        # Retornamos el objeto Servicio.
        return self._servicio

    # Propiedad de solo lectura para obtener la cantidad reservada.
    @property
    def cantidad(self) -> float:
        # Retornamos la cantidad solicitada.
        return self._cantidad

    # Propiedad de solo lectura para obtener el estado actual de la reserva.
    @property
    def estado(self) -> str:
        # Retornamos el estado actual.
        return self._estado

    # Propiedad de solo lectura para obtener el costo total calculado.
    @property
    def costo_total(self) -> float:
        # Retornamos el costo total.
        return self._costo_total

    # Método para calcular o recalcular el costo con parámetros opcionales (sobrecarga vía argumentos por defecto).
    def calcular_costo(self, cantidad: float = None, descuento_pct: float = None, porcentaje_impuesto: float = None) -> float:
        # Usamos la cantidad indicada o la cantidad guardada en la reserva.
        cant_usar = self._cantidad if cantidad is None else cantidad
        # Usamos el descuento indicado o el descuento guardado en la reserva.
        desc_usar = self._descuento_pct if descuento_pct is None else descuento_pct
        # Usamos el impuesto indicado o el impuesto guardado en la reserva.
        imp_usar = self._porcentaje_impuesto if porcentaje_impuesto is None else porcentaje_impuesto
        # Delegamos el cálculo al método polimórfico del servicio asociado.
        return self._servicio.calcular_costo(cant_usar, desc_usar, imp_usar)

    # Método para confirmar una reserva pendiente.
    def confirmar(self) -> None:
        # Verificamos que la reserva no esté cancelada.
        if self._estado == "CANCELADA":
            # Lanzamos ReservaInvalidaError si se intenta confirmar una reserva cancelada.
            raise ReservaInvalidaError(f"No se puede confirmar la reserva '{self._id_reserva}' porque está CANCELADA.")
        # Cambiamos el estado a CONFIRMADA.
        self._estado = "CONFIRMADA"

    # Método para cancelar una reserva activa o pendiente.
    def cancelar(self) -> None:
        # Verificamos que la reserva no esté ya cancelada.
        if self._estado == "CANCELADA":
            # Lanzamos ReservaInvalidaError si ya estaba cancelada.
            raise ReservaInvalidaError(f"La reserva '{self._id_reserva}' ya se encuentra CANCELADA.")
        # Cambiamos el estado a CANCELADA.
        self._estado = "CANCELADA"

    # Método que devuelve un resumen legible de la reserva.
    def resumen(self) -> str:
        # Construimos y retornamos la cadena con los datos principales de la reserva.
        return f"Reserva [{self._id_reserva}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | Total: ${self._costo_total:.2f}"
