# 🧪 tests/test_main.py

Tests unitarios para `main.py`. Verifica el flujo de arranque de la partida y el manejo de entradas inválidas.

---

# Módulo bajo prueba
`main` → `iniciar_partida`

---

# Clase `TestMain`

## `test_iniciar_partida_flujo_completo`
Simula una ejecución completa de `iniciar_partida()` con 2 jugadores (`"Ana"` y `"Bert"`). Usa `@patch` sobre `JuegoChinchon`, `TerminalUI`, `input` y `print`.

Verifica que:
- Se llame a `ui.limpiar()` exactamente **1 vez** al inicio.
- `input` se llame **3 veces** (número de jugadores + 2 nombres).
- `JuegoChinchon` se instancie con `(["Ana", "Bert"], mock_ui)`.
- Se llame a `juego.jugar()` exactamente **1 vez**.

---

## `test_iniciar_partida_error_input_no_numerico`
Verifica que si el usuario introduce un valor no numérico como número de jugadores, la función lance `ValueError` (dado que `int()` falla con texto).

---

# Ejecución

```bash
pytest tests/test_main.py -v
```