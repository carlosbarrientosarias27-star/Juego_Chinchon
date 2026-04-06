# 🃏 Juego Chinchón

Implementación en Python del clásico juego de cartas español **Chinchón**, jugable en terminal con soporte para 2 a 4 jugadores, comodines especiales de cerveza y detección automática de combinaciones ganadoras.

---

# 📁 Estructura del proyecto

```
JUEGO_CHINCHON/
├── core/
│   ├── cards.py          # Baraja española y carta inmutable
│   ├── engine.py         # Motor principal y bucle de juego
│   └── validator.py      # Validación de combinaciones y puntuación
├── models/
│   └── player.py         # Modelo de datos del jugador
├── ui/
│   ├── interface.py      # Contrato abstracto de interfaz de usuario
│   └── terminal.py       # Implementación CLI de la interfaz
├── tests/
│   ├── test_cards.py
│   ├── test_engine.py
│   ├── test_interface.py
│   ├── test_main.py
│   ├── test_player.py
│   ├── test_terminal.py
│   └── test_validator.py
├── docs/                 # Documentación individual por módulo
├── main.py               # Punto de entrada
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

# 🚀 Instalación y ejecución

**Requisitos:** Python 3.10+

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/juego-chinchon.git
cd juego-chinchon

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python main.py
```

**Ejecutar tests:**

```bash
pytest
```

---

# 🎮 Reglas del juego

## Objetivo
Ser el último jugador en pie. Un jugador es **eliminado** cuando acumula **100 puntos o más**. El ganador es quien permanezca con menos de 100 puntos cuando todos los demás hayan sido eliminados.

---

## La baraja
Se juega con baraja española de **40 cartas** (4 palos × 10 valores) más **4 comodines** especiales:

| Palo     | Valores disponibles       |
|----------|---------------------------|
| Oros     | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12 |
| Copas    | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12 |
| Espadas  | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12 |
| Bastos   | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12 |

> ⚠️ Los valores 8 y 9 **no existen** en la baraja española.

---

## Desarrollo de una ronda

1. Se reparten **7 cartas** a cada jugador.
2. Se coloca una carta boca arriba como inicio del **pozo de descartes**.
3. Los jugadores se turnan en orden. En cada turno:
   - **Robar:** el jugador elige robar del **mazo** o del **pozo**.
   - **Descartar:** el jugador descarta una carta de su mano al pozo.
4. Un jugador puede **cerrar la ronda** al descartar si sus puntos son **≤ 15**.
5. Al cerrar, se cuentan los puntos de todos y se acumulan.

---

## Puntuación

Cada carta vale su valor numérico en puntos. Las cartas que forman **combinaciones válidas** no suman puntos:

| Combinación | Descripción                                              | Mínimo |
|-------------|----------------------------------------------------------|--------|
| **Grupo**   | 3 o más cartas del mismo valor (distintos palos)         | 3      |
| **Escalera**| 3 o más cartas consecutivas del mismo palo               | 3      |

El objetivo de cada jugador es minimizar los puntos de las cartas que **no** pertenecen a ninguna combinación.

---

## Chinchón 🏆
Si un jugador logra que sus **7 cartas formen una sola combinación válida** (escalera o grupo de 7), hace **Chinchón** y recibe una bonificación de **-10 puntos**.

---

## Comodines de cerveza 🍺
Al robar del mazo, un jugador puede obtener uno de los 4 comodines especiales. Cada uno tiene un efecto inmediato:

| ID | Comodín          | Efecto                                                        |
|----|------------------|---------------------------------------------------------------|
| 1  | Estrella Galicia | Reduce los puntos del jugador a **80** si tenía ≥ 100        |
| 2  | Alhambra Verde   | Reduce los puntos del jugador a **25** si tenía ≥ 50         |
| 3  | 1906             | Resta **25 puntos** al jugador si tenía ≥ 25                 |
| 4  | SIN CERVEZA      | **Elimina** al jugador inmediatamente de la partida          |

Tras aplicar el efecto, el jugador roba una carta normal y continúa su turno.

---

## Eliminación
Un jugador queda **eliminado** si:
- Acumula **100 puntos o más** al final de una ronda.
- Roba el comodín **SIN CERVEZA** (nº 4).

---

## Salir de la partida
En cualquier momento de su turno, un jugador puede escribir `S` para **abandonar la partida**, lo que la finaliza inmediatamente.

---

# 📚 Documentación

Cada módulo tiene su propio README en la carpeta `docs/`:

| Archivo              | Módulo documentado     |
|----------------------|------------------------|
| `cards.md`           | `core/cards.py`        |
| `engine.md`          | `core/engine.py`       |
| `validator.md`       | `core/validator.py`    |
| `player.md`          | `models/player.py`     |
| `interface.md`       | `ui/interface.py`      |
| `terminal.md`        | `ui/terminal.py`       |
| `main.md`            | `main.py`              |

---

# 🛠️ Tecnologías

- **Python 3.10+**
- `dataclasses` — modelos inmutables
- `abc` — contrato de interfaz desacoplado
- `itertools` — búsqueda de combinaciones
- `pytest` — suite de tests