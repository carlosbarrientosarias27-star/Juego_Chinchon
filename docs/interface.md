# 🎮 ui/interface.py

Contrato abstracto que define la interfaz de usuario del juego.

---

# Descripción

`GameInterface` es una clase base abstracta (`ABC`) que establece el conjunto de métodos que **cualquier implementación de UI debe respetar**. No contiene lógica propia; su propósito es desacoplar el motor del juego (`engine.py`) de la tecnología de presentación concreta (terminal, web, GUI, etc.).

La implementación actual de este contrato es `ui/terminal.py` → `TerminalUI`.

---

# `GameInterface` — clase abstracta

```python
from abc import ABC, abstractmethod

class GameInterface(ABC):
    ...
```

Todas las subclases deben implementar los siguientes métodos marcados con `@abstractmethod`. Instanciar `GameInterface` directamente lanzará `TypeError`.

---

# Métodos abstractos

## `limpiar_pantalla() → None`
Limpia el buffer visual de la interfaz actual (pantalla, canvas, etc.).

---

## `mostrar_mensaje(mensaje: str) → None`
Muestra un mensaje informativo genérico al usuario.

```python
ui.mostrar_mensaje("Es el turno de Ana.")
```

---

## `mostrar_estado_juego(jugadores: List[Jugador], carta_descarte: Optional[Carta]) → None`
Muestra la situación general de la mesa: puntuaciones de todos los jugadores y la carta visible en el pozo de descartes.

```python
ui.mostrar_estado_juego(juego.jugadores, baraja.descartes[-1])
```

---

## `solicitar_accion_robo(jugador: Jugador, carta_descarte: Carta) → str`
Solicita al jugador que elija de dónde robar en su turno.

| Retorno esperado | Significado                    |
|------------------|--------------------------------|
| `"mazo"`         | Robar del mazo                 |
| `"descarte"`     | Robar del pozo de descartes    |
| `"salir"`        | Salir voluntariamente          |

```python
opcion = ui.solicitar_accion_robo(jugador, carta_tope)
```

---

## `solicitar_descarte(jugador: Jugador, puede_cerrar: bool) → Tuple[int, bool]`
Solicita al jugador qué carta desea descartar y si quiere cerrar la ronda.

Retorna una tupla `(indice_carta, quiere_cerrar)`:

| Valor           | Tipo   | Descripción                                   |
|-----------------|--------|-----------------------------------------------|
| `indice_carta`  | `int`  | Posición (0-based) de la carta a descartar    |
| `quiere_cerrar` | `bool` | `True` si el jugador confirma cerrar la ronda |

```python
idx, cerrar = ui.solicitar_descarte(jugador, puede_cerrar=True)
```

---

## `notificar_comodin(nombre: str, id_comodin: int) → None`
Muestra una alerta visual cuando un jugador roba un comodín de cerveza.

```python
ui.notificar_comodin("Alhambra Verde", 2)
```

---

## `mostrar_resultado_ronda(jugadores: List[Jugador], cerrador: Jugador) → None`
Muestra el desglose de puntos de todos los jugadores al finalizar una ronda, indicando quién fue el cerrador.

```python
ui.mostrar_resultado_ronda(juego.jugadores, jugador_que_cerro)
```

---

## `anunciar_ganador(ganador: Optional[Jugador]) → None`
Muestra el mensaje final de fin de partida.

- Si `ganador` es un `Jugador`, muestra su nombre como vencedor.
- Si `ganador` es `None`, indica que la partida terminó sin ganador claro.

```python
ui.anunciar_ganador(ganador)   # Con ganador
ui.anunciar_ganador(None)      # Sin ganador
```

---

# Implementar una UI personalizada

Para crear una nueva interfaz (ej. gráfica o web), basta con heredar de `GameInterface` e implementar todos sus métodos:

```python
from ui.interface import GameInterface

class MiUI(GameInterface):
    def limpiar_pantalla(self): ...
    def mostrar_mensaje(self, mensaje): ...
    def mostrar_estado_juego(self, jugadores, carta_descarte): ...
    def solicitar_accion_robo(self, jugador, carta_descarte): ...
    def solicitar_descarte(self, jugador, puede_cerrar): ...
    def notificar_comodin(self, nombre, id_comodin): ...
    def mostrar_resultado_ronda(self, jugadores, cerrador): ...
    def anunciar_ganador(self, ganador): ...
```

---

# Dependencias

| Módulo          | Uso                                        |
|-----------------|--------------------------------------------|
| `abc`           | `ABC` y `abstractmethod`                   |
| `typing`        | Anotaciones `List`, `Tuple`, `Optional`    |
| `models.player` | Tipo `Jugador` en las firmas de métodos    |
| `core.cards`    | Tipo `Carta` en las firmas de métodos      |