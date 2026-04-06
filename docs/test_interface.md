# 🧪 tests/test_interface.py

Tests unitarios para `ui/interface.py`. Verifica el comportamiento del contrato abstracto `GameInterface`.

---

# Módulo bajo prueba
`ui.interface` → `GameInterface`

---

# Tests

## `test_no_se_puede_instanciar_clase_abstracta`
Verifica que intentar instanciar `GameInterface` directamente lance `TypeError` con el mensaje `"Can't instantiate abstract class GameInterface"`.

---

## `test_subclase_incompleta_lanza_error`
Verifica que una subclase que implementa solo parte de los métodos abstractos (`limpiar_pantalla` únicamente) también lance `TypeError` al intentar instanciarse.

---

## `test_subclase_valida_instanciacion`
Verifica que una subclase que implementa **todos** los métodos abstractos del contrato pueda instanciarse sin errores y sea reconocida como instancia de `GameInterface`.

Los métodos implementados en la subclase de prueba son: `limpiar_pantalla`, `mostrar_mensaje`, `mostrar_estado_juego`, `solicitar_accion_robo`, `solicitar_descarte`, `notificar_comodin`, `mostrar_resultado_ronda` y `anunciar_ganador`.

---

# Ejecución

```bash
pytest tests/test_interface.py -v
```