# ⚙️ core/engine.py

Motor principal del juego. Controla el flujo completo de la partida, la gestión de turnos y las reglas de negocio del Chinchón.

---

# Descripción

`JuegoChinchon` es el orquestador central de la partida. Coordina jugadores, baraja, validador e interfaz de usuario para ejecutar el ciclo completo del juego: preparación de rondas, turnos individuales, efectos de comodines y cálculo de puntuaciones.

---

# `JuegoChinchon`

```python
class JuegoChinchon:
    def __init__(self, nombres_jugadores: List[str], ui: GameInterface)
```

## Atributos de instancia

| Atributo        | Tipo            | Descripción                                      |
|-----------------|-----------------|--------------------------------------------------|
| `ui`            | `GameInterface` | Interfaz de usuario inyectada                    |
| `jugadores`     | `List[Jugador]` | Lista completa de jugadores de la partida        |
| `baraja`        | `Baraja`        | Instancia de la baraja activa                    |
| `ronda_actual`  | `int`           | Número de ronda en curso (empieza en 1)          |
| `finalizado`    | `bool`          | Estado de finalización de la partida             |

---

# Métodos

## `obtener_jugadores_activos() → List[Jugador]`
Filtra y retorna solo los jugadores que no han sido eliminados.

```python
activos = juego.obtener_jugadores_activos()
```

---

## `preparar_ronda()`
Reinicia la baraja, coloca una carta inicial en la pila de descartes y reparte **7 cartas** a cada jugador activo.

```python
juego.preparar_ronda()
```

---

## `ejecutar_turno(jugador: Jugador) → bool`
Gestiona el turno completo de un jugador en dos fases:

**Fase 1 — Robo:**
- El jugador elige robar del **mazo** o del **descarte**.
- Si roba un comodín desde el mazo, se aplica su efecto especial y luego roba una carta normal.

**Fase 2 — Descarte/Cierre:**
- El jugador descarta una carta de su mano.
- Si sus puntos son ≤ 15, puede optar por **cerrar la ronda**.

Retorna `True` si el jugador decide cerrar, `False` en caso contrario.

```python
cerrar = juego.ejecutar_turno(jugador)
if cerrar:
    juego.calcular_fin_ronda(jugador)
```

---

## `calcular_fin_ronda(cerrador: Jugador)`
Procesa la puntuación de todos los jugadores activos al cierre de una ronda:

- Si un jugador tiene **Chinchón** (7 cartas en combo válido), resta 10 puntos.
- En caso contrario, suma los puntos de las cartas no combinadas.
- Los jugadores que alcancen o superen **100 puntos** son **eliminados**.

```python
juego.calcular_fin_ronda(jugador_que_cerro)
```

---

## `_aplicar_logica_comodin(jugador: Jugador, carta: Carta)` *(privado)*
Aplica el efecto de un comodín de cerveza sobre el jugador que lo robó.

| ID | Nombre          | Efecto                                              |
|----|-----------------|-----------------------------------------------------|
| 1  | Estrecha Galicia | Reduce puntos a 80 si el jugador tiene ≥ 100        |
| 2  | Alhambra Verde  | Reduce puntos a 25 si el jugador tiene ≥ 50         |
| 3  | 1906            | Resta 25 puntos si el jugador tiene ≥ 25            |
| 4  | SIN CERVEZA     | **Elimina** al jugador inmediatamente               |

---

## `jugar()`
**Bucle principal de la partida.** Ejecuta rondas completas hasta que solo quede un jugador activo. Al finalizar, anuncia al ganador.

```python
juego = JuegoChinchon(['Ana', 'Luis', 'María'], ui=mi_interfaz)
juego.jugar()
```

**Flujo interno:**
```
mientras haya > 1 jugador activo:
    preparar_ronda()
    para cada jugador en orden:
        ejecutar_turno()
        si cierra → calcular_fin_ronda() → nueva ronda
mostrar_puntuaciones()
anunciar_ganador()
```

---

# Dependencias internas

| Módulo              | Uso                                        |
|---------------------|--------------------------------------------|
| `models.player`     | Clase `Jugador`                            |
| `core.cards`        | Clases `Baraja` y `Carta`                  |
| `core.validator`    | `Validador.calcular_puntos_optimos()`      |
| `ui.interface`      | `GameInterface` para interacción con el UI |