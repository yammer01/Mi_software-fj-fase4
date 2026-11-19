# src/excepciones.py
# Importamos el módulo datetime para incluir marcas de tiempo en mensajes de error si se requiere.
from datetime import datetime


# Clase base personalizada que hereda de Exception para representar errores del sistema Software FJ.
class ErrorSoftwareFJ(Exception):
    # Constructor que recibe el mensaje de error y un código opcional de contexto.
    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Guardamos el código de error específico en la instancia.
        self.codigo = codigo
        # Registramos la fecha y hora exacta en que ocurrió la excepción.
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construimos un mensaje descriptivo con código y marca de tiempo.
        mensaje_completo = f"[{self.fecha_hora}] [{self.codigo}] {mensaje}"
        # Llamamos al constructor de la clase padre Exception con el mensaje formateado.
        super().__init__(mensaje_completo)


# Excepción específica para datos de cliente inválidos o incompletos.
class ClienteInvalidoError(ErrorSoftwareFJ):
    # Constructor que delega a ErrorSoftwareFJ asignando un código propio.
    def __init__(self, mensaje: str):
        # Invocamos al constructor padre con el código ERR_CLIENTE.
        super().__init__(mensaje, codigo="ERR_CLIENTE")


# Excepción específica para parámetros inválidos o creación incorrecta de servicios.
class ServicioInvalidoError(ErrorSoftwareFJ):
    # Constructor que delega a ErrorSoftwareFJ asignando el código ERR_SERVICIO.
    def __init__(self, mensaje: str):
        # Invocamos al constructor padre con el código ERR_SERVICIO.
        super().__init__(mensaje, codigo="ERR_SERVICIO")


# Excepción específica cuando un servicio no está disponible o ocurre un conflicto.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    # Constructor que delega a ErrorSoftwareFJ asignando el código ERR_DISPONIBILIDAD.
    def __init__(self, mensaje: str):
        # Invocamos al constructor padre con el código ERR_DISPONIBILIDAD.
        super().__init__(mensaje, codigo="ERR_DISPONIBILIDAD")


# Excepción específica para operaciones inválidas en reservas.
class ReservaInvalidaError(ErrorSoftwareFJ):
    # Constructor que delega a ErrorSoftwareFJ asignando el código ERR_RESERVA.
    def __init__(self, mensaje: str):
        # Invocamos al constructor padre con el código ERR_RESERVA.
        super().__init__(mensaje, codigo="ERR_RESERVA")
