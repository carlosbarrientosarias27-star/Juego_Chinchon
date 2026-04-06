# 🖥️ ui/terminal.py

Implementación de la interfaz de usuario para entornos de terminal (CLI).

---

# Descripción

`TerminalUI` gestiona toda la interacción con el jugador a través de la consola: renderizado de cartas, visualización de la mano, entrada de acciones y anuncio de resultados. Actúa como implementación concreta de la interfaz de usuario del juego.

---

# `TerminalUI`

No requiere inicialización con parámetros.

```python
ui = TerminalUI()
```

---

# Métodos

## `limpiar()`
Limpia la pantalla de la terminal de forma segura, compatible con Windows (`cls`) y Unix/Linux/macOS (`clear`).

Usa `subprocess.run` con `shell=False` para evitar inyección de comandos. Si el comando falla, continúa silenciosamente sin interrumpir el juego.

```python
ui.limpiar()
```

---

## `render_carta(carta: Carta) → str`
Genera la representación visual en texto de una carta.

| Tipo de carta | Formato de salida         |
|---------------|---------------------------|
| Normal        | `[7 de Oros]`             |
| Comodín       | `[🍺 Comodín 2]`          |

```python
ui.render_carta(Carta('Oros', 7))                      # → "[7 de Oros]"
ui.render_carta(Carta(es_comodin=True, id_comodin=2))  # → "[🍺 Comodín 2]"
```

---

## `mostrar_mano(jugador: Jugador)`
Imprime en consola la mano completa del jugador con índices numerados desde 1.

```
👉 Mano de Ana:
  1. [3 de Copas]
  2. [7 de Oros]
  3. [🍺 Comodín 1]
  ...
```

```python
ui.mostrar_mano(jugador)
```

---

## `anunciar_ganador(ganador: Optional[Jugador])`
Imprime el resultado final de la partida.

- Si hay ganador, muestra su nombre enmarcado.
- Si `ganador` es `None`, informa que la partida terminó sin ganador claro.

```
==============================
¡EL GANADOR ES: Ana!
==============================
```

```python
ui.anunciar_ganador(jugador)   # Con ganador
ui.anunciar_ganador(None)      # Sin ganador
```

---

## `solicitar_accion_robo(jugador: Jugador, carta_descarte: Carta) → str`
Muestra la mano del jugador y la carta en el pozo, luego solicita la acción de robo.

Repite la pregunta hasta recibir una entrada válida.

| Entrada | Retorno    | Acción                        |
|---------|------------|-------------------------------|
| `M`     | `"mazo"`   | Robar del mazo                |
| `P`     | `"pozo"`   | Robar del pozo (descarte)     |
| `S`     | `"salir"`  | Salir voluntariamente         |

```python
opcion = ui.solicitar_accion_robo(jugador, carta_tope)
# → "mazo" | "pozo" | "salir"
```

---

## `solicitar_descarte(jugador: Jugador, puede_cerrar: bool) → tuple[int, bool]`
Muestra la mano y pide al jugador que elija una carta para descartar. Si `puede_cerrar` es `True`, también pregunta si desea cerrar la ronda.

Valida que el índice sea un número dentro del rango. Repite la pregunta en caso de entrada inválida.

Retorna una tupla `(indice, quiere_cerrar)`:

| Valor          | Tipo   | Descripción                                     |
|----------------|--------|-------------------------------------------------|
| `indice`       | `int`  | Posición (0-based) de la carta a descartar      |
| `quiere_cerrar`| `bool` | `True` si el jugador confirmó cerrar la ronda   |

```python
idx, cerrar = ui.solicitar_descarte(jugador, puede_cerrar=True)
carta_descartada = jugador.extraer_de_mano(idx)
```

---

# Ejemplo de flujo completo

```python
from ui.terminal import TerminalUI
from core.engine import JuegoChinchon

ui = TerminalUI()
juego = JuegoChinchon(['Ana', 'Luis'], ui=ui)
juego.jugar()
```

---

# Dependencias

| Módulo       | Uso                                         |
|--------------|---------------------------------------------|
| `subprocess` | Ejecutar `cls`/`clear` de forma segura      |
| `os`         | Detectar el sistema operativo (`os.name`)   |