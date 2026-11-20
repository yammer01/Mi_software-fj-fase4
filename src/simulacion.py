# simulacion.py
# Importamos las clases de servicios concretos desde src/modelos.py.
from src.modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Importamos el gestor principal desde src/gestor.py.
from src.gestor import GestorSoftwareFJ
# Importamos las excepciones personalizadas para capturarlas o registrarlas de forma ordenada durante la simulación.
from src.excepciones import ErrorSoftwareFJ


# Función principal que ejecuta las 10 operaciones de prueba de el sistema en memoria.
def ejecutar_simulacion() -> None:
    # Instanciamos el gestor principal con su archivo exclusivo de registro de eventos y errores.
    gestor = GestorSoftwareFJ(ruta_log="logs/software_fj.log")
    # Registramos el inicio de la simulación en el archivo de log.
    gestor.registrar_log("INFO", "=== Inicio de simulación de 10 operaciones - Software FJ Fase 4 ===")

    # Contador auxiliar para numerar cada una de las 10 operaciones.
    operaciones_exitosas = 0
    # Contador auxiliar para las excepciones controladas durante la simulación.
    errores_controlados = 0

    # --- OPERACIÓN 1: Registrar primer cliente válido ---
    try:
        # Registramos al cliente CLI-01 con datos completos y válidos.
        cliente_1 = gestor.registrar_cliente("CLI-01", "Laura Gómez", "laura.gomez@correo.com", "1098765432")
        # Mostramos confirmación en consola.
        print(f"[Op 1 - OK] {cliente_1.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Si ocurre un error del sistema, lo reportamos sin detener la ejecución.
        print(f"[Op 1 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 2: Registrar segundo cliente válido ---
    try:
        # Registramos al cliente CLI-02 con datos válidos.
        cliente_2 = gestor.registrar_cliente("CLI-02", "Carlos Ruiz", "carlos.ruiz@empresa.co", "80123456")
        # Mostramos confirmación en consola.
        print(f"[Op 2 - OK] {cliente_2.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos error controlado sin detener el flujo.
        print(f"[Op 2 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 3: Intentar registrar un cliente inválido (correo sin '@') ---
    try:
        # Intentamos registrar un cliente con correo inválido para disparar ClienteInvalidoError.
        gestor.registrar_cliente("CLI-03", "Andrés Pérez", "correo_invalido.com", "11223344")
        # Esta línea no se ejecutará si se lanza la excepción esperada.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Capturamos y mostramos que el sistema registró el error y continuó sin romperse.
        print(f"[Op 3 - ERROR REGISTRADO EN LOG] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 4: Registrar servicio de sala disponible ---
    try:
        # Creamos una instancia de ReservaSala con capacidad de 12 personas y tarifa por hora.
        sala_a = ReservaSala("SRV-SALA-1", "Sala Ejecutiva A", 80.0, capacidad=12, disponible=True)
        # Registramos el servicio en el gestor.
        gestor.registrar_servicio(sala_a)
        # Mostramos el resumen polimórfico del servicio.
        print(f"[Op 4 - OK] Servicio registrado: {sala_a.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos si ocurre algún error de servicio.
        print(f"[Op 4 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 5: Registrar servicio de alquiler de equipo y marcarlo no disponible ---
    try:
        # Creamos un servicio AlquilerEquipo para proyectores/cámaras.
        equipo_cam = AlquilerEquipo("SRV-EQ-1", "Kit Cámara HD", 45.0, tipo_equipo="Audiovisual", disponible=True)
        # Marcamos el equipo como no disponible para probar validación de disponibilidad.
        equipo_cam.set_disponible(False)
        # Registramos el servicio en el gestor.
        gestor.registrar_servicio(equipo_cam)
        # Mostramos el estado actual del servicio.
        print(f"[Op 5 - OK] Servicio registrado (no disponible): {equipo_cam.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos si ocurre algún error al registrar el servicio.
        print(f"[Op 5 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 6: Crear una reserva válida sobre la sala disponible ---
    try:
        # Creamos la reserva RES-01 para CLI-01 en SRV-SALA-1 por 3 horas con 10% de descuento e 5% de impuesto.
        reserva_1 = gestor.crear_reserva("RES-01", "CLI-01", "SRV-SALA-1", cantidad=3, descuento_pct=10.0, porcentaje_impuesto=5.0)
        # Mostramos el resumen de la reserva creada.
        print(f"[Op 6 - OK] {reserva_1.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos si ocurre error al crear la reserva.
        print(f"[Op 6 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 7: Intentar crear una reserva sobre servicio no disponible ---
    try:
        # Intentamos reservar SRV-EQ-1 que está marcado como no disponible (debe lanzar ServicioNoDisponibleError).
        gestor.crear_reserva("RES-02", "CLI-02", "SRV-EQ-1", cantidad=2)
        # No se ejecutará si se lanza la excepción esperada.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Verificamos que el error de disponibilidad quedó registrado y el flujo sigue.
        print(f"[Op 7 - ERROR REGISTRADO EN LOG] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 8: Calcular costo con variantes opcionales (descuento, impuesto y recargo) ---
    try:
        # Calculamos el costo variante de SRV-SALA-1 para 4 horas con descuento, impuesto y recargo fijo.
        total_variante = gestor.calcular_costo_variante(
            id_servicio="SRV-SALA-1",
            cantidad=4,
            descuento_pct=5.0,
            porcentaje_impuesto=19.0,
            recargo_fijo=15.0,
        )
        # Mostramos el costo calculado con variantes.
        print(f"[Op 8 - OK] Cálculo variante SRV-SALA-1 (4h): ${total_variante:.2f}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos si ocurre algún error en el cálculo variante.
        print(f"[Op 8 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 9: Confirmar la reserva válida RES-01 ---
    try:
        # Confirmamos la reserva RES-01 pasando su estado a CONFIRMADA.
        reserva_confirmada = gestor.confirmar_reserva("RES-01")
        # Mostramos la reserva ya confirmada.
        print(f"[Op 9 - OK] {reserva_confirmada.resumen()}")
        # Aumentamos el contador de operaciones exitosas.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Reportamos si ocurre error al confirmar.
        print(f"[Op 9 - ERROR CONTROLADO] {exc}")
        errores_controlados += 1

    # --- OPERACIÓN 10: Intentar confirmar una reserva inexistente (error controlado) ---
    try:
        # Buscamos y confirmamos una reserva que no existe para probar ReservaInvalidaError.
        gestor.confirmar_reserva("RES-999")
        # No se ejecutará si se lanza la excepción esperada.
        operaciones_exitosas += 1
    except ErrorSoftwareFJ as exc:
        # Confirmamos que el error quedó registrado en el log y el programa finaliza limpio.
        print(f"[Op 10 - ERROR REGISTRADO EN LOG] {exc}")
        errores_controlados += 1

    # Registramos el cierre de la simulación en el archivo de log.
    gestor.registrar_log("INFO", f"=== Fin de simulación | Exitosas: {operaciones_exitosas} | Errores controlados: {errores_controlados} ===")
    # Imprimimos el resumen final en consola.
    print("\n--- RESUMEN FINAL DE SIMULACIÓN ---")
    print(f"Operaciones exitosas: {operaciones_exitosas}")
    print(f"Errores controlados registrados en log: {errores_controlados}")
    print(f"Archivo de log generado en: {gestor.ruta_log}")


# Punto de entrada estándar cuando se ejecuta simulacion.py directamente.
if __name__ == "__main__":
    # Invocamos la función principal de simulación.
    ejecutar_simulacion()
