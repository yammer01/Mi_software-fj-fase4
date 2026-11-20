# Mi_software-fj-fase4
Sistema de gestión de servicios, clientes y reservas - Fase 4

## Ejecución local y verificación (Fase 4)

Para correr la simulación desde la carpeta raíz del proyecto (donde está `src`):

```bash
python -m src.simulacion
```
Ajustes y correcciones que tocó hacer
src/simulacion.py (línea 79): se cambió equipo_cam.establecer_disponible(False) por equipo_cam.set_disponible(False) porque el método real en la clase Servicio (src/modelos.py) se llama así y estaba generando un AttributeError.

src/reserva.py (línea 34): se cambió servicio.parametros_validacion(cantidad) por servicio.validar_parametros(cantidad) para alinearlo con el método definido en Servicio (src/modelos.py) y evitar que frenara la creación de reservas.
