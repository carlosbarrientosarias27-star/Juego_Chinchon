# 🧪 tests/test_engine.py

Tests unitarios para `core/engine.py`. Verifica la inicialización del motor, la gestión de turnos, los efectos de comodines, el cálculo de puntuaciones y la salida voluntaria del juego.

---

# Módulo bajo prueba
`core.engine` → `JuegoChinchon`

---

# Fixtures

| Fixture    | Descripción                                              |
|------------|----------------------------------------------------------|
| `mock_ui`  | `MagicMock` que simula `GameInterface` sin bloqueos de input |
| `juego`    | Instancia de `JuegoChinchon` con 2 jugadores y `mock_ui` |

---

# Clase `TestJuegoChinchon`

## `test_inicializacion`
Verifica que el estado inicial del motor sea correcto: 2 jugadores, `ronda_actual == 1` y `finalizado == False`.

---

## `test_obtener_jugadores_activos`
Elimina un jugador manualmente y comprueba que `obtener_jugadores_activos()` excluya a los jugadores con `eliminado = True`.

---

## `test_aplicar_logica_comodin_muerte`
Verifica que el comodín con `id_comodin=4` (SIN CERVEZA) establezca `jugador.eliminado = True`.

---

## `test_ejecutar_turno_basico`
Simula un turno completo donde el jugador roba del mazo y no cierra. Verifica que:
- `ejecutar_turno()` retorne `False`.
- La mano del jugador mantenga **7 cartas** tras descartar.
- `baraja.robar()` se llame exactamente **1 vez**.

Usa `@patch` sobre `Validador.calcular_puntos_optimos`.

---

## `test_calcular_fin_ronda_chinchon`
Simula que un jugador hace Chinchón (`calcular_puntos_optimos` retorna `(0, True)`). Verifica que:
- Los puntos del jugador se reduzcan en **10** (`15 → 5`).
- Se notifique el evento `"¡... hizo CHINCHÓN! (-10 pts)"`.

---

## `test_ejecutar_turno_salir`
Simula que el jugador elige `"salir"` durante la fase de robo. Verifica que `ejecutar_turno()` retorne `None`.

---

## `test_jugar_interrupcion_por_salida`
Verifica que el bucle principal `jugar()` termine limpiamente cuando `ejecutar_turno()` retorna `None`. Confirma que `calcular_fin_ronda()` **no** llegue a llamarse.

---

# Ejecución

```bash
pytest tests/test_engine.py -v
```