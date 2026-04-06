# 🧪 tests/test_player.py

Tests unitarios para `models/player.py`. Verifica la inicialización del jugador, gestión de la mano, manejo de comodines y representación en texto.

---

# Módulo bajo prueba
`models.player` → `Jugador`

---

# Fixture

| Fixture        | Descripción                                          |
|----------------|------------------------------------------------------|
| `jugador_test` | Instancia limpia de `Jugador(nombre="Cervezero")` para cada test |

---

# Clase `TestJugador`

## `test_inicializacion_por_defecto`
Verifica los valores iniciales de un jugador recién creado: `puntos == 0`, `eliminado == False`, mano vacía y todos los comodines en `False`.

---

## `test_añadir_a_mano`
Verifica que `añadir_a_mano()` agregue correctamente una carta mock a la mano y que `cantidad_cartas` incremente a `1`.

---

## `test_extraer_de_mano_valido`
Verifica que `extraer_de_mano(0)` retorne la carta correcta y deje la mano vacía.

---

## `test_extraer_de_mano_indice_invalido`
Verifica que `extraer_de_mano(99)` lance `IndexError` con el mensaje `"El índice de la carta no existe"`.

---

## `test_gestion_comodines`
Verifica el ciclo completo del uso de comodines:
- `tiene_comodin_usado(3)` retorna `False` inicialmente.
- Tras `marcar_comodin_usado(3)`, retorna `True`.

---

## `test_propiedad_cantidad_cartas`
Verifica que la propiedad `cantidad_cartas` se actualice dinámicamente al modificar `jugador.mano` directamente.

---

## `test_representacion_string`
Verifica `__str__` en dos estados:
- Estado normal: contiene el nombre y `"0 pts"`.
- Estado eliminado: contiene `"ELIMINADO"`.

---

# Ejecución

```bash
pytest tests/test_player.py -v
```