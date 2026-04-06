# 🧪 tests/test_cards.py

Tests unitarios para `core/cards.py`. Verifica la inicialización de la baraja, el robo de cartas, la puntuación y el reabastecimiento automático del mazo.

---

# Módulo bajo prueba
`core.cards` → `Baraja`, `Carta`

---

# Tests

## `test_baraja_inicializacion`
Verifica que al crear una `Baraja` el mazo contenga exactamente **44 cartas** (40 normales + 4 comodines).

---

## `test_robar_carta`
Verifica que `robar()` retorne una instancia de `Carta` y que el mazo quede con **43 cartas** tras el robo.

---

## `test_puntos_comodin`
Verifica que `obtener_puntos()` retorne `0` para una carta comodín.

---

## `test_puntos_normales`
Verifica que `obtener_puntos()` retorne el valor numérico correcto para una carta normal (ej. `7 de Oros` → `7`).

---

## `test_reabastecer_mazo`
Verifica el comportamiento de reabastecimiento automático cuando el mazo está vacío:

- Configura el mazo vacío con 3 cartas en descartes.
- Llama a `robar()`, lo que activa la lógica de reabastecimiento.
- Comprueba que el mazo quede con **1 carta** y los descartes con **1 carta** (la última reservada).

---

## `test_baraja_reiniciar`
Verifica que `reiniciar()` restaure el estado inicial de la baraja:

- Simula una partida avanzada (10 robos + 2 descartes).
- Llama a `reiniciar()`.
- Comprueba que el mazo vuelva a tener **44 cartas** y los descartes queden **vacíos**.

---

# Ejecución

```bash
pytest tests/test_cards.py -v
```