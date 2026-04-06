# 🃏 Juego Chinchón

Implementación en Python del clásico juego de cartas español **Chinchón**, jugable en terminal con soporte para 2 a 4 jugadores, comodines especiales de cerveza y detección automática de combinaciones ganadoras.

---

# 📁 Estructura del proyecto

```
JUEGO_CHINCHON/
├── .github/
│   └── workflows/
│       └── pipeline.yml      # Pipeline de CI/CD (tests automáticos)
├── core/
│   ├── __init__.py
│   ├── cards.py              # Baraja española y carta inmutable
│   ├── engine.py             # Motor principal y bucle de juego
│   └── validator.py          # Validación de combinaciones y puntuación
├── models/
│   ├── __init__.py
│   └── player.py             # Modelo de datos del jugador
├── ui/
│   ├── __init__.py
│   ├── interface.py          # Contrato abstracto de interfaz de usuario
│   └── terminal.py           # Implementación CLI de la interfaz
├── tests/
│   ├── test_cards.py         # Tests de Baraja y Carta
│   ├── test_engine.py        # Tests del motor de juego
│   ├── test_interface.py     # Tests del contrato abstracto UI
│   ├── test_main.py          # Tests del punto de entrada
│   ├── test_player.py        # Tests del modelo Jugador
│   ├── test_terminal.py      # Tests de la interfaz CLI
│   └── test_validator.py     # Tests del validador de combinaciones
├── docs/                     # Documentación individual por módulo
│   ├── cards.md
│   ├── engine.md
│   ├── validator.md
│   ├── player.md
│   ├── interface.md
│   ├── terminal.md
│   ├── main.md
│   ├── test_cards.md
│   ├── test_engine.md
│   ├── test_interface.md
│   ├── test_main.md
│   ├── test_player.md
│   ├── test_terminal.md
│   ├── test_validator.md
│   ├── asistencia_ia.md
│   ├── Errores de seguridad.md
│   └── Pruebas de comodin y caso edge.md
├── .gitignore
├── conftest.py
├── main.py                   # Punto de entrada
├── pytest.ini
├── requirements.txt
└── README.md
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

---

# 🧪 Tests

El proyecto cuenta con una suite completa de **tests unitarios** con `pytest`, cubriendo todos los módulos del juego.

## Ejecutar todos los tests

```bash
pytest
```

## Ejecutar con detalle

```bash
pytest -v
```

## Ejecutar un módulo específico

```bash
pytest tests/test_cards.py -v
pytest tests/test_engine.py -v
```

## Cobertura de tests por módulo

| Archivo de test       | Módulo cubierto        | Nº tests | Qué verifica                                           |
|-----------------------|------------------------|----------|--------------------------------------------------------|
| `test_cards.py`       | `core/cards.py`        | 6        | Inicialización, robo, puntos, reabastecimiento, reinicio |
| `test_engine.py`      | `core/engine.py`       | 6        | Motor, turnos, comodines, Chinchón, salida voluntaria  |
| `test_interface.py`   | `ui/interface.py`      | 3        | Contrato ABC, subclases completas e incompletas        |
| `test_main.py`        | `main.py`              | 2        | Flujo de arranque, manejo de input inválido            |
| `test_player.py`      | `models/player.py`     | 7        | Mano, extracción, comodines, propiedades, `__str__`    |
| `test_terminal.py`    | `ui/terminal.py`       | 9        | Render, limpieza, entradas, reintentos, descarte       |
| `test_validator.py`   | `core/validator.py`    | 8        | Escaleras, grupos, puntuación óptima, Chinchón         |

---

# ⚙️ CI/CD

El proyecto utiliza **GitHub Actions** con un pipeline definido en `.github/workflows/pipeline.yml` que se ejecuta automáticamente en cada `push` o `pull request`.

## Flujo del pipeline

```
Push / Pull Request
      ↓
Instalar dependencias (pip install -r requirements.txt)
      ↓
Ejecutar suite de tests (pytest)
      ↓
✅ Tests pasan → merge permitido
❌ Tests fallan → merge bloqueado
```

## Badge de estado

![CI](https://github.com/tu-usuario/juego-chinchon/actions/workflows/pipeline.yml/badge.svg)

> Sustituye `tu-usuario` por tu nombre de usuario de GitHub para activar el badge.

---

# 🎮 Reglas del juego

## Objetivo
Ser el último jugador en pie. Un jugador es **eliminado** cuando acumula **100 puntos o más**. El ganador es quien permanezca con menos de 100 puntos cuando todos los demás hayan sido eliminados.

---

## La baraja
Se juega con baraja española de **40 cartas** (4 palos × 10 valores) más **4 comodines** especiales:

| Palo     | Valores disponibles                    |
|----------|----------------------------------------|
| Oros     | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12       |
| Copas    | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12       |
| Espadas  | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12       |
| Bastos   | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12       |

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

| Combinación  | Descripción                                      | Mínimo |
|--------------|--------------------------------------------------|--------|
| **Grupo**    | 3 o más cartas del mismo valor (distintos palos) | 3      |
| **Escalera** | 3 o más cartas consecutivas del mismo palo       | 3      |

---

## Chinchón 🏆
Si un jugador logra que sus **7 cartas formen una sola combinación válida**, hace **Chinchón** y recibe una bonificación de **-10 puntos**.

---

## Comodines de cerveza 🍺
Al robar del mazo, un jugador puede obtener uno de los 4 comodines especiales:

| ID | Comodín          | Efecto                                                     |
|----|------------------|------------------------------------------------------------|
| 1  | Estrella Galicia | Reduce los puntos del jugador a **80** si tenía ≥ 100      |
| 2  | Alhambra Verde   | Reduce los puntos del jugador a **25** si tenía ≥ 50       |
| 3  | 1906             | Resta **25 puntos** al jugador si tenía ≥ 25               |
| 4  | SIN CERVEZA      | **Elimina** al jugador inmediatamente de la partida        |

Tras aplicar el efecto, el jugador roba una carta normal y continúa su turno.

---

## Eliminación
Un jugador queda **eliminado** si:
- Acumula **100 puntos o más** al final de una ronda.
- Roba el comodín **SIN CERVEZA** (nº 4).

---

## Salir de la partida
En cualquier momento de su turno, un jugador puede introducir `S` para **abandonar la partida**, lo que la finaliza inmediatamente.

---

# 📚 Documentación

Cada módulo tiene su propio README en la carpeta `docs/`:

| Archivo                          | Módulo documentado     |
|----------------------------------|------------------------|
| `cards.md`                       | `core/cards.py`        |
| `engine.md`                      | `core/engine.py`       |
| `validator.md`                   | `core/validator.py`    |
| `player.md`                      | `models/player.py`     |
| `interface.md`                   | `ui/interface.py`      |
| `terminal.md`                    | `ui/terminal.py`       |
| `main.md`                        | `main.py`              |
| `test_cards.md`                  | `tests/test_cards.py`  |
| `test_engine.md`                 | `tests/test_engine.py` |
| `test_interface.md`              | `tests/test_interface.py` |
| `test_main.md`                   | `tests/test_main.py`   |
| `test_player.md`                 | `tests/test_player.py` |
| `test_terminal.md`               | `tests/test_terminal.py` |
| `test_validator.md`              | `tests/test_validator.py` |

---

# 🛠️ Tecnologías

- **Python 3.10+**
- `dataclasses` — modelos inmutables
- `abc` — contrato de interfaz desacoplado
- `itertools` — búsqueda de combinaciones
- `pytest` — suite de tests unitarios
- **GitHub Actions** — CI/CD automático