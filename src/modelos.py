# src/modelos.py
# Importamos ABC y abstractmethod para definir clases abstractas y métodos obligatorios.
from abc import ABC, abstractmethod
# Importamos las excepciones personalizadas creadas en src/excepciones.py.
from src.excepciones import ClienteInvalidoError, ServicioInvalidoError


# Clase abstracta base para entidades generales del sistema.
class EntidadSistema(ABC):
    # Constructor común que valida y asigna un identificador único.
    def __init__(self, id_entidad: str):
        # Validamos que el identificador sea una cadena no vacía.
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            # Lanzamos ValueError si el ID no es válido.
            raise ValueError("El identificador de la entidad debe ser un texto no vacío.")
        # Encapsulamos el identificador en un atributo protegido.
        self._id = id_entidad.strip()

    # Propiedad de solo lectura para consultar el ID de la entidad.
    @property
    def id(self) -> str:
        # Retornamos el identificador encapsulado.
        return self._id

    # Método abstracto que cada subclase debe implementar para resumir su estado.
    @abstractmethod
    def resumen(self) -> str:
        # Las subclases concretas definen su propia representación.
        pass


# Clase Cliente que hereda de EntidadSistema y encapsula datos personales con validaciones.
class Cliente(EntidadSistema):
    # Constructor de Cliente con id, nombre, correo y documento.
    def __init__(self, id_cliente: str, nombre: str, correo: str, documento: str):
        # Invocamos el constructor de EntidadSistema para validar y guardar _id.
        super().__init__(id_cliente)
        # Validamos y asignamos el nombre usando la propiedad/setter correspondiente.
        self.nombre = nombre
        # Validamos y asignamos el correo electrónico.
        self.correo = correo
        # Validamos y asignamos el documento de identidad.
        self.documento = documento

    # Getter para obtener el nombre del cliente.
    @property
    def nombre(self) -> str:
        # Retornamos el nombre encapsulado.
        return self._nombre

    # Setter con validación estricta para el nombre.
    @nombre.setter
    def nombre(self, valor: str):
        # Verificamos que sea texto y tenga al menos 2 caracteres útiles.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            # Lanzamos excepción personalizada si el nombre es inválido.
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 2 caracteres.")
        # Guardamos el valor limpio.
        self._nombre = valor.strip()

    # Getter para obtener el correo del cliente.
    @property
    def correo(self) -> str:
        # Retornamos el correo encapsulado.
        return self._correo

    # Setter con validación estricta para el correo electrónico.
    @correo.setter
    def correo(self, valor: str):
        # Verificamos que sea texto y contenga '@' y un punto tras el dominio.
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            # Lanzamos excepción personalizada si el correo no tiene formato válido.
            raise ClienteInvalidoError("El correo electrónico del cliente no es válido.")
        # Guardamos el correo en minúsculas y sin espacios extra.
        self._correo = valor.strip().lower()

    # Getter para obtener el documento del cliente.
    @property
    def documento(self) -> str:
        # Retornamos el documento encapsulado.
        return self._documento

    # Setter con validación estricta para el documento.
    @documento.setter
    def documento(self, valor: str):
        # Verificamos que el documento tenga al menos 5 caracteres alfanuméricos.
        if not isinstance(valor, str) or len(valor.strip()) < 5:
            # Lanzamos excepción personalizada si el documento es muy corto o inválido.
            raise ClienteInvalidoError("El documento del cliente debe tener al menos 5 caracteres.")
        # Guardamos el documento limpio.
        self._documento = valor.strip()

    # Implementación del método abstracto resumen exigido por EntidadSistema.
    def resumen(self) -> str:
        # Devolvemos una descripción clara del cliente.
        return f"Cliente [{self._id}] - {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"


# Clase abstracta Servicio que hereda de EntidadSistema para modelar servicios de Software FJ.
class Servicio(EntidadSistema, ABC):
    # Constructor base para cualquier servicio con id, nombre, tarifa base y disponibilidad.
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Inicializamos la entidad base con su identificador.
        super().__init__(id_servicio)
        # Validamos que el nombre del servicio no esté vacío.
        if not isinstance(nombre, str) or not nombre.strip():
            # Lanzamos excepción personalizada si falta o es inválido el nombre.
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        # Validamos que la tarifa base sea numérica y mayor que cero.
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            # Lanzamos excepción personalizada si la tarifa es cero o negativa.
            raise ServicioInvalidoError("La tarifa base del servicio debe ser mayor que cero.")
        # Asignamos el nombre limpio.
        self._nombre = nombre.strip()
        # Convertimos y guardamos la tarifa base como flotante.
        self._tarifa_base = float(tarifa_base)
        # Guardamos si el servicio está disponible para reservar.
        self._disponible = bool(disponible)

    # Propiedad para consultar el nombre del servicio.
    @property
    def nombre(self) -> str:
        # Retornamos el nombre.
        return self._nombre

    # Propiedad para consultar la tarifa base.
    @property
    def tarifa_base(self) -> float:
        # Retornamos la tarifa base.
        return self._tarifa_base

    # Propiedad para consultar si está disponible.
    @property
    def disponible(self) -> bool:
        # Retornamos el estado de disponibilidad.
        return self._disponible

    # Método para cambiar la disponibilidad del servicio.
    def set_disponible(self, estado: bool):
        # Actualizamos el estado booleano de disponibilidad.
        self._disponible = bool(estado)

    # Método abstracto para validar parámetros específicos de cada tipo de servicio.
    @abstractmethod
    def validar_parametros(self, cantidad: float, **kwargs):
        # Cada subclase validará duración, unidades o condiciones propias.
        pass

    # Método abstracto para calcular el costo según la cantidad/duración y parámetros opcionales.
    @abstractmethod
    def calcular_costo(self, cantidad: float, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Cada subclase definirá su fórmula de cálculo de costo.
        pass

    # Método abstracto para describir el servicio de forma polimórfica.
    @abstractmethod
    def describir(self) -> str:
        # Cada subclase retornará su descripción detallada.
        pass

    # Implementación de resumen usando describir para cumplir EntidadSistema.
    def resumen(self) -> str:
        # Retornamos la descripción del servicio.
        return self.describir()


# Subclase 1: Reserva de salas (costo por horas y capacidad de asistentes).
class ReservaSala(Servicio):
    # Constructor de ReservaSala incluyendo capacidad máxima de la sala.
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        # Validamos que la capacidad de la sala sea al menos 1 persona.
        if not isinstance(capacidad, int) or capacidad < 1:
            # Lanzamos excepción si la capacidad es inválida.
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero mayor o igual a 1.")
        # Llamamos al constructor de Servicio.
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        # Guardamos la capacidad máxima de la sala.
        self._capacidad = capacidad

    # Validamos horas de reserva y número de asistentes si se envía.
    def validar_parametros(self, cantidad: float, **kwargs):
        # Validamos que la cantidad de horas sea positiva.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si las horas no son válidas.
            raise ServicioInvalidoError("La duración en horas para la sala debe ser mayor que cero.")
        # Obtenemos los asistentes opcionales desde kwargs.
        asistentes = kwargs.get("asistentes")
        # Si se indicaron asistentes, validamos que no superen la capacidad de la sala.
        if asistentes is not None and (not isinstance(asistentes, int) or asistentes <= 0 or asistentes > self._capacidad):
            # Lanzamos excepción si excede la capacidad o es inválido.
            raise ServicioInvalidoError(f"Asistentes inválidos o superiores a la capacidad ({self._capacidad}).")

    # Calculamos costo por horas con soporte a descuento e impuesto opcionales (sobrecarga vía parámetros).
    def calcular_costo(self, cantidad: float, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Validamos que las horas sean positivas antes de calcular.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si la duración es inválida.
            raise ServicioInvalidoError("La cantidad de horas debe ser mayor que cero para calcular el costo.")
        # Calculamos el subtotal multiplicando tarifa por horas.
        subtotal = self._tarifa_base * float(cantidad)
        # Aplicamos descuento porcentual si corresponde.
        con_descuento = subtotal * (1 - (descuento_pct / 100.0))
        # Aplicamos impuesto porcentual si corresponde y redondeamos a 2 decimales.
        total = con_descuento * (1 + (impuesto_pct / 100.0))
        # Retornamos el total redondeado.
        return round(total, 2)

    # Descripción polimórfica del servicio de reserva de sala.
    def describir(self) -> str:
        # Formamos el texto de estado de disponibilidad.
        estado = "Disponible" if self._disponible else "No disponible"
        # Retornamos la descripción completa.
        return f"[Sala] {self._nombre} | Cap: {self._capacidad} | Tarifa/h: ${self._tarifa_base:.2f} | {estado}"


# Subclase 2: Alquiler de equipos (costo por días/unidades).
class AlquilerEquipo(Servicio):
    # Constructor de AlquilerEquipo incluyendo el tipo de equipo.
    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, tipo_equipo: str, disponible: bool = True):
        # Validamos que el tipo de equipo sea una cadena no vacía.
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            # Lanzamos excepción si falta el tipo de equipo.
            raise ServicioInvalidoError("Debe especificar el tipo de equipo a alquilar.")
        # Llamamos al constructor de Servicio.
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        # Guardamos el tipo de equipo.
        self._tipo_equipo = tipo_equipo.strip()

    # Validamos que la cantidad de días sea positiva.
    def validar_parametros(self, cantidad: float, **kwargs):
        # Verificamos que la cantidad de días sea mayor que cero.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si los días son inválidos.
            raise ServicioInvalidoError("La cantidad de días de alquiler debe ser mayor que cero.")

    # Calculamos costo por días con descuento e impuesto opcionales.
    def calcular_costo(self, cantidad: float, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Validamos que los días sean positivos.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si los días son inválidos.
            raise ServicioInvalidoError("La cantidad de días debe ser mayor que cero para calcular el costo.")
        # Calculamos subtotal por días.
        subtotal = self._tarifa_base * float(cantidad)
        # Aplicamos descuento porcentual.
        con_descuento = subtotal * (1 - (descuento_pct / 100.0))
        # Aplicamos impuesto porcentual.
        total = con_descuento * (1 + (impuesto_pct / 100.0))
        # Retornamos el valor redondeado a 2 decimales.
        return round(total, 2)

    # Descripción polimórfica del servicio de alquiler de equipos.
    def describir(self) -> str:
        # Formamos el texto de estado.
        estado = "Disponible" if self._disponible else "No disponible"
        # Retornamos la descripción del equipo.
        return f"[Equipo: {self._tipo_equipo}] {self._nombre} | Tarifa/día: ${self._tarifa_base:.2f} | {estado}"


# Subclase 3: Asesorías especializadas (costo por sesiones/horas de consultoría).
class AsesoriaEspecializada(Servicio):
    # Constructor de AsesoriaEspecializada incluyendo especialidad del consultor.
    def __init__(self, id_servicio: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        # Validamos que la especialidad no esté vacía.
        if not isinstance(especialidad, str) or not especialidad.strip():
            # Lanzamos excepción si falta la especialidad.
            raise ServicioInvalidoError("Debe indicar la especialidad de la asesoría.")
        # Llamamos al constructor de Servicio.
        super().__init__(id_servicio, nombre, tarifa_sesion, disponible)
        # Guardamos la especialidad.
        self._especialidad = especialidad.strip()

    # Validamos que el número de sesiones sea válido.
    def validar_parametros(self, cantidad: float, **kwargs):
        # Verificamos que la cantidad de sesiones sea mayor que cero.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si las sesiones son inválidas.
            raise ServicioInvalidoError("La cantidad de sesiones de asesoría debe ser mayor que cero.")

    # Calculamos costo por sesiones con descuento e impuesto opcionales.
    def calcular_costo(self, cantidad: float, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Validamos que el número de sesiones sea positivo.
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            # Lanzamos excepción si las sesiones son inválidas.
            raise ServicioInvalidoError("La cantidad de sesiones debe ser mayor que cero para calcular el costo.")
        # Calculamos subtotal.
        subtotal = self._tarifa_base * float(cantidad)
        # Aplicamos descuento porcentual.
        con_descuento = subtotal * (1 - (descuento_pct / 100.0))
        # Aplicamos impuesto porcentual.
        total = con_descuento * (1 + (impuesto_pct / 100.0))
        # Retornamos total redondeado.
        return round(total, 2)

    # Descripción polimórfica del servicio de asesoría especializada.
    def describir(self) -> str:
        # Formamos el texto de estado.
        estado = "Disponible" if self._disponible else "No disponible"
        # Retornamos la descripción de la asesoría.
        return f"[Asesoría - {self._especialidad}] {self._nombre} | Tarifa/sesión: ${self._tarifa_base:.2f} | {estado}"
