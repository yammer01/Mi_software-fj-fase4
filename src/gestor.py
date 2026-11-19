# src/gestor.py
# Importamos os para asegurar que la carpeta de logs exista si se indica una ruta con directorio.
import os
# Importamos datetime para registrar marcas de tiempo en el archivo de log.
from datetime import datetime
# Importamos las clases de modelos y reserva desde el paquete src.
from src.modelos import Cliente, Servicio
from src.reserva import Reserva
# Importamos las excepciones personalizadas desde src/excepciones.py.
from src.excepciones import (
    ErrorSoftwareFJ,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
)


# Clase gestora principal que administra clientes, servicios, reservas y el registro de logs en memoria.
class GestorSoftwareFJ:
    # Constructor que inicializa las colecciones en memoria y la ruta del archivo exclusivo de log.
    def __init__(self, ruta_log: str = "logs/software_fj.log"):
        # Lista en memoria para almacenar los clientes registrados.
        self._clientes: list[Cliente] = []
        # Lista en memoria para almacenar los servicios disponibles y no disponibles.
        self._servicios: list[Servicio] = []
        # Lista en memoria para almacenar las reservas creadas.
        self._reservas: list[Reserva] = []
        # Guardamos la ruta del archivo de log exclusivo para eventos y errores.
        self._ruta_log = ruta_log
        # Preparamos el directorio y el archivo de log al inicializar el gestor.
        self._preparar_archivo_log()

    # Método auxiliar para garantizar que el archivo de log exista antes de escribir.
    def _preparar_archivo_log(self) -> None:
        # Obtenemos la carpeta contenedora de la ruta del log si existe.
        carpeta = os.path.dirname(self._ruta_log)
        # Si la ruta incluye una carpeta, la creamos si aún no existe.
        if carpeta:
            # Creamos directorios intermedios sin error si ya existen.
            os.makedirs(carpeta, exist_ok=True)
        # Abrimos el archivo en modo anexar ('a') con codificación UTF-8 y lo cerramos automáticamente.
        with open(self._ruta_log, "a", encoding="utf-8"):
            # No necesitamos escribir nada al crear el archivo vacío.
            pass

    # Método centralizado para escribir eventos y errores con marca de tiempo en el archivo de log.
    def registrar_log(self, nivel: str, mensaje: str) -> None:
        # Generamos la marca de tiempo actual con formato legible.
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Formateamos la línea que se guardará en el log.
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        # Usamos bloque try/except/finally para escribir de forma segura en el archivo de log.
        archivo = None
        try:
            # Abrimos el archivo de log en modo anexar ('a') con codificación UTF-8.
            archivo = open(self._ruta_log, "a", encoding="utf-8")
            # Escribimos la línea formateada en el archivo.
            archivo.write(linea)
        except OSError as exc:
            # Si ocurre un error de entrada/salida al escribir el log, lo imprimimos en consola sin detener la app.
            print(f"Advertencia: no se pudo escribir en el archivo de log '{self._ruta_log}': {exc}")
        finally:
            # Cerramos el archivo explícitamente si quedó abierto.
            if archivo is not None and not archivo.closed:
                # Cerramos el descriptor de archivo.
                archivo.close()

    # Método para registrar un nuevo cliente en memoria con manejo completo de excepciones.
    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, documento: str) -> Cliente:
        # Iniciamos bloque try para construir y validar el cliente.
        try:
            # Verificamos si ya existe un cliente con el mismo ID en la lista en memoria.
            if any(c.id == id_cliente.strip() for c in self._clientes if isinstance(id_cliente, str)):
                # Lanzamos excepción específica de cliente inválido por ID duplicado.
                raise ClienteInvalidoError(f"Ya existe un cliente registrado con el ID '{id_cliente.strip()}'.")
            # Instanciamos la clase Cliente ejecutando sus validaciones internas.
            nuevo_cliente = Cliente(id_cliente, nombre, correo, documento)
        except ClienteInvalidoError as exc:
            # Registramos el error de cliente en el archivo de log.
            self.registrar_log("ERROR", f"Fallo al registrar cliente ({id_cliente}): {exc}")
            # Propagamos la excepción personalizada.
            raise
        except ValueError as exc:
            # Encadenamos el ValueError original dentro de ClienteInvalidoError usando 'raise ... from ...'.
            error_encadenado = ClienteInvalidoError(f"Datos inválidos al crear cliente '{id_cliente}': {exc}")
            # Registramos el error encadenado en el archivo de log.
            self.registrar_log("ERROR", f"Error encadenado al registrar cliente ({id_cliente}): {error_encadenado}")
            # Lanzamos la nueva excepción conservando la causa original.
            raise error_encadenado from exc
        else:
            # Si no hubo excepciones, agregamos el cliente a la lista en memoria.
            self._clientes.append(nuevo_cliente)
            # Registramos el evento exitoso en el archivo de log.
            self.registrar_log("INFO", f"Cliente registrado correctamente: {nuevo_cliente.resumen()}")
            # Retornamos el cliente creado.
            return nuevo_cliente
        finally:
            # Registramos un trazo de auditoría indicando que finalizó el intento de registro de cliente.
            self.registrar_log("DEBUG", f"Finalizó intento de registrar_cliente con ID='{id_cliente}'.")

    # Método para registrar un servicio (subclase de Servicio) en memoria.
    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        # Iniciamos bloque try para validar y almacenar el servicio.
        try:
            # Validamos que el objeto recibido sea instancia de Servicio.
            if not isinstance(servicio, Servicio):
                # Lanzamos ServicioInvalidoError si el objeto no corresponde a Servicio.
                raise ServicioInvalidoError("Solo se pueden registrar instancias válidas de la clase Servicio.")
            # Verificamos que no exista ya un servicio con el mismo ID.
            if any(s.id == servicio.id for s in self._servicios):
                # Lanzamos ServicioInvalidoError por duplicidad de ID.
                raise ServicioInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")
        except ServicioInvalidoError as exc:
            # Registramos el error en el archivo de log.
            self.registrar_log("ERROR", f"Fallo al registrar servicio: {exc}")
            # Re-lanzamos la excepción.
            raise
        else:
            # Agregamos el servicio a la lista en memoria.
            self._servicios.append(servicio)
            # Registramos el alta del servicio en el log.
            self.registrar_log("INFO", f"Servicio registrado: {servicio.resumen()}")
            # Retornamos el servicio registrado.
            return servicio
        finally:
            # Registramos el cierre de la operación de registro de servicio.
            self.registrar_log("DEBUG", "Finalizó intento de registrar_servicio.")

    # Método auxiliar para buscar un cliente por ID en memoria.
    def buscar_cliente(self, id_cliente: str) -> Cliente:
        # Recorremos la lista de clientes en memoria.
        for cliente in self._clientes:
            # Comparamos el ID del cliente con el ID buscado.
            if cliente.id == id_cliente:
                # Retornamos el cliente encontrado.
                return cliente
        # Si no se encuentra, lanzamos ClienteInvalidoError.
        raise ClienteInvalidoError(f"No se encontró ningún cliente con el ID '{id_cliente}'.")

    # Método auxiliar para buscar un servicio por ID en memoria.
    def buscar_servicio(self, id_servicio: str) -> Servicio:
        # Recorremos la lista de servicios en memoria.
        for servicio in self._servicios:
            # Comparamos el ID del servicio con el ID buscado.
            if servicio.id == id_servicio:
                # Retornamos el servicio encontrado.
                return servicio
        # Si no se encuentra, lanzamos ServicioInvalidoError.
        raise ServicioInvalidoError(f"No se encontró ningún servicio con el ID '{id_servicio}'.")

    # Método auxiliar para buscar una reserva por ID en memoria.
    def buscar_reserva(self, id_reserva: str) -> Reserva:
        # Recorremos la lista de reservas en memoria.
        for reserva in self._reservas:
            # Comparamos el ID de la reserva con el ID buscado.
            if reserva.id_reserva == id_reserva:
                # Retornamos la reserva encontrada.
                return reserva
        # Si no se encuentra, lanzamos ReservaInvalidaError.
        raise ReservaInvalidaError(f"No se encontró ninguna reserva con el ID '{id_reserva}'.")

    # Método para crear y almacenar una nueva reserva vinculando cliente y servicio existentes.
    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, cantidad: float, descuento_pct: float = 0.0, porcentaje_impuesto: float = 0.0) -> Reserva:
        # Iniciamos bloque try para buscar entidades y construir la reserva.
        try:
            # Verificamos que el ID de reserva no esté repetido en memoria.
            if any(r.id_reserva == id_reserva for r in self._reservas):
                # Lanzamos ReservaInvalidaError si el ID ya existe.
                raise ReservaInvalidaError(f"Ya existe una reserva con el ID '{id_reserva}'.")
            # Buscamos el cliente en memoria (puede lanzar ClienteInvalidoError).
            cliente = self.buscar_cliente(id_cliente)
            # Buscamos el servicio en memoria (puede lanzar ServicioInvalidoError).
            servicio = self.buscar_servicio(id_servicio)
            # Creamos la instancia de Reserva validando disponibilidad y parámetros.
            nueva_reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                cantidad=cantidad,
                descuento_pct=descuento_pct,
                porcentaje_impuesto=porcentaje_impuesto,
            )
        except (ClienteInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError) as exc:
            # Registramos cualquiera de estas excepciones del dominio en el log.
            self.registrar_log("ERROR", f"Fallo al crear reserva '{id_reserva}': {exc}")
            # Propagamos la excepción.
            raise
        except (TypeError, ValueError) as exc:
            # Encadenamos errores de tipo o valor dentro de ReservaInvalidaError.
            error_encadenado = ReservaInvalidaError(f"Parámetros inválidos en reserva '{id_reserva}': {exc}")
            # Registramos el error encadenado en el archivo de log.
            self.registrar_log("ERROR", f"Error encadenado al crear reserva '{id_reserva}': {error_encadenado}")
            # Lanzamos la excepción encadenada con 'from exc'.
            raise error_encadenado from exc
        else:
            # Guardamos la reserva en la lista en memoria si todo salió bien.
            self._reservas.append(nueva_reserva)
            # Registramos el evento exitoso en el archivo de log.
            self.registrar_log("INFO", f"Reserva creada: {nueva_reserva.resumen()}")
            # Retornamos la reserva creada.
            return nueva_reserva
        finally:
            # Registramos la finalización del intento de creación de reserva.
            self.registrar_log("DEBUG", f"Finalizó intento de crear_reserva con ID='{id_reserva}'.")

    # Método para confirmar una reserva existente en memoria.
    def confirmar_reserva(self, id_reserva: str) -> Reserva:
        # Iniciamos bloque try para localizar y confirmar la reserva.
        try:
            # Buscamos la reserva por ID.
            reserva = self.buscar_reserva(id_reserva)
            # Ejecutamos la transición a CONFIRMADA.
            reserva.confirmar()
        except ReservaInvalidaError as exc:
            # Registramos el error en el archivo de log.
            self.registrar_log("ERROR", f"Fallo al confirmar reserva '{id_reserva}': {exc}")
            # Propagamos la excepción.
            raise
        else:
            # Registramos la confirmación exitosa en el log.
            self.registrar_log("INFO", f"Reserva confirmada: {reserva.resumen()}")
            # Retornamos la reserva confirmada.
            return reserva
        finally:
            # Registramos el cierre de la operación de confirmación.
            self.registrar_log("DEBUG", f"Finalizó intento de confirmar_reserva con ID='{id_reserva}'.")

    # Método para cancelar una reserva existente en memoria.
    def cancelar_reserva(self, id_reserva: str) -> Reserva:
        # Iniciamos bloque try para localizar y cancelar la reserva.
        try:
            # Buscamos la reserva por ID.
            reserva = self.buscar_reserva(id_reserva)
            # Ejecutamos la transición a CANCELADA.
            reserva.cancelar()
        except ReservaInvalidaError as exc:
            # Registramos el error en el archivo de log.
            self.registrar_log("ERROR", f"Fallo al cancelar reserva '{id_reserva}': {exc}")
            # Propagamos la excepción.
            raise
        else:
            # Registramos la cancelación exitosa en el log.
            self.registrar_log("INFO", f"Reserva cancelada: {reserva.resumen()}")
            # Retornamos la reserva cancelada.
            return reserva
        finally:
            # Registramos el cierre de la operación de cancelación.
            self.registrar_log("DEBUG", f"Finalizó intento de cancelar_reserva con ID='{id_reserva}'.")

    # Método con variantes/sobrecarga mediante argumentos opcionales para calcular costos de un servicio.
    def calcular_costo_variante(self, id_servicio: str, cantidad: float = 1.0, descuento_pct: float = 0.0, porcentaje_impuesto: float = 0.0, recargo_fijo: float = 0.0) -> float:
        # Iniciamos bloque try para calcular el costo con las variantes indicadas.
        try:
            # Buscamos el servicio en memoria.
            servicio = self.buscar_servicio(id_servicio)
            # Calculamos el costo base con descuento e impuesto usando el método polimórfico del servicio.
            subtotal_calculado = servicio.calcular_costo(cantidad, descuento_pct, porcentaje_impuesto)
            # Validamos que el recargo fijo opcional sea numérico y no negativo.
            if not isinstance(recargo_fijo, (int, float)) or recargo_fijo < 0:
                # Lanzamos ServicioInvalidoError si el recargo fijo no es válido.
                raise ServicioInvalidoError("El recargo fijo opcional debe ser un número mayor o igual a cero.")
            # Sumamos el recargo fijo opcional y redondeamos a dos decimales.
            total_final = round(subtotal_calculado + float(recargo_fijo), 2)
        except (ServicioInvalidoError, ValueError, TypeError) as exc:
            # Encadenamos el error en ServicioInvalidoError si no lo es ya.
            if isinstance(exc, ServicioInvalidoError):
                # Registramos y re-lanzamos ServicioInvalidoError.
                self.registrar_log("ERROR", f"Error en variante de costo para servicio '{id_servicio}': {exc}")
                raise
            # Encadenamos errores inesperados de cálculo.
            error_encadenado = ServicioInvalidoError(f"No se pudo calcular el costo para servicio '{id_servicio}': {exc}")
            # Registramos el error encadenado en el log.
            self.registrar_log("ERROR", f"Error encadenado en calcular_costo_variante: {error_encadenado}")
            # Lanzamos con encadenamiento explícito.
            raise error_encadenado from exc
        else:
            # Registramos el cálculo exitoso en el archivo de log.
            self.registrar_log("INFO", f"Costo calculado para servicio '{id_servicio}' (cant={cantidad}, desc={descuento_pct}%, imp={porcentaje_impuesto}%, recargo=${recargo_fijo:.2f}): ${total_final:.2f}")
            # Retornamos el total final calculado.
            return total_final
        finally:
            # Registramos el cierre de la operación de cálculo.
            self.registrar_log("DEBUG", f"Finalizó calcular_costo_variante para servicio='{id_servicio}'.")

    # Propiedades de consulta para inspeccionar las colecciones en memoria.
    @property
    def clientes(self) -> list[Cliente]:
        # Retornamos una copia superficial de la lista de clientes.
        return list(self._clientes)

    @property
    def servicios(self) -> list[Servicio]:
        # Retornamos una copia superficial de la lista de servicios.
        return list(self._servicios)

    @property
    def reservas(self) -> list[Reserva]:
        # Retornamos una copia superficial de la lista de reservas.
        return list(self._reservas)

    @property
    def ruta_log(self) -> str:
        # Retornamos la ruta del archivo de log.
        return self._ruta_log
