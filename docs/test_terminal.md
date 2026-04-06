# 🧪 tests/test_terminal.py

Tests unitarios para `ui/terminal.py`. Verifica el renderizado de cartas, la limpieza de pantalla, la visualización de la mano y la gestión de entradas del usuario.

---

# Módulo bajo prueba
`ui.terminal` → `TerminalUI`

---

# Fixture

| Fixture | Descripción                        |
|---------|------------------------------------|
| `ui`    | Instancia de `TerminalUI` por test |

---

# Clase `TestTerminalUI`

## `test_limpiar_windows`
Parchea `os.name` como `'nt'` y verifica que `limpiar()` llame a `subprocess.run(['cls'], check=True)`.

---

## `test_limpiar_unix`
Parchea `os.name` como `'posix'` y verifica que `limpiar()` llame a `subprocess.run(['clear'], check=True)`.

---

## `test_render_carta_normal`
Verifica que `render_carta()` retorne el formato `"[7 de Oros]"` para una carta normal.

---

## `test_render_carta_comodin`
Verifica que `render_carta()` incluya `"[🍺 Comodín 3]"` para una carta comodín con `id_comodin=3`.

---

## `test_mostrar_mano`
Verifica que `mostrar_mano()` imprima el encabezado `"\n👉 Mano de Alice:"` con `print`.

---

## `test_anunciar_ganador`
Verifica que `anunciar_ganador()` imprima el mensaje `"¡EL GANADOR ES: Carlos!"`.

---

## `test_solicitar_accion_robo_reintento`
Simula entradas `['X', 'M']`: verifica que una entrada inválida (`X`) sea rechazada y que en el segundo intento (`M`) se retorne `"mazo"`.

---

## `test_solicitar_descarte_cerrando`
Simula entradas `['2', 'S']` con `puede_cerrar=True`. Verifica que se retorne `(1, True)` — índice 1 (base 0) y cierre confirmado.

---

## `test_solicitar_accion_robo_salir`
Verifica que al introducir `'S'`, `solicitar_accion_robo()` retorne `"salir"`.

---

# Ejecución

```bash
pytest tests/test_terminal.py -v
```