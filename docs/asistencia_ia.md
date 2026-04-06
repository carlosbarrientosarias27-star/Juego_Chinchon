# 🃏 Juego Chincón — Prompts Utilizados en el Desarrollo

Este documento recoge los prompts empleados durante el desarrollo del proyecto **Juego_Chincón** con asistencia de IA (Claude). Están organizados por módulo y fase de desarrollo.

---

# 📁 Estructura del Proyecto

```
JUEGO_CHINCHON/
├── core/
│   ├── cards.py
│   ├── engine.py
│   └── validator.py
├── models/
│   └── player.py
├── ui/
│   ├── interface.py
│   └── terminal.py
├── tests/
│   ├── test_cards.py
│   ├── test_engine.py
│   ├── test_interface.py
│   ├── test_main.py
│   ├── test_player.py
│   ├── test_terminal.py
│   └── test_validator.py
├── docs/
│   └── Errores de seguridad.md
├── main.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

# 🚀 Fase 1 — Diseño Inicial del Proyecto

## Prompt de arranque general

```
Quiero desarrollar el juego de cartas español "Chincón" en Python.
El juego debe poder jugarse en la terminal.
Crea la estructura de carpetas y ficheros base del proyecto con los módulos:
- core/ (lógica del juego: cartas, motor, validador)
- models/ (jugadores)
- ui/ (interfaz de terminal)
- tests/ (pruebas unitarias con pytest)
Incluye un main.py como punto de entrada y un requirements.txt.
```

---

# 🃏 Fase 2 — Módulo `core/cards.py`

## Creación del mazo

```
Crea la clase `Deck` en Python para representar una baraja española de 40 cartas.
Cada carta debe tener palo (oros, copas, espadas, bastos) y valor numérico (1-7, 10-12).
Incluye métodos para barajar el mazo y repartir cartas.
```

## Representación de cartas

```
Añade una clase `Card` con atributos `suit` y `value`.
Implementa __repr__ y __eq__ para facilitar comparaciones y depuración.
```

---

# ⚙️ Fase 3 — Módulo `core/engine.py`

## Motor principal del juego

```
Desarrolla la clase `GameEngine` que gestione el flujo completo de una partida de Chincón.
Debe controlar:
- El turno de cada jugador
- Robar carta del mazo o del descarte
- Descartar una carta
- Detectar cuándo un jugador puede declarar Chincón
- Calcular puntuaciones al final de la ronda
```

## Lógica de turnos

```
Implementa la lógica de turnos en `GameEngine` de forma que cada jugador
pueda robar una carta (del mazo o del montón de descarte) y descartar una.
El turno pasa automáticamente al siguiente jugador en orden circular.
```

---

# ✅ Fase 4 — Módulo `core/validator.py`

## Validación de jugadas

```
Crea la clase `Validator` con métodos para validar:
- Si la mano de un jugador contiene grupos válidos (escaleras o tríos/cuartetos)
- Si un jugador puede declarar Chincón (todas las cartas forman combinaciones válidas)
- El cálculo de puntos de las cartas no combinadas (puntos de penalización)
```

## Seguridad en las entradas

```
Revisa el módulo validator.py y añade validaciones de seguridad para las entradas del usuario.
Evita errores inesperados ante valores nulos, tipos incorrectos o datos fuera de rango.
Documenta los casos de error en docs/Errores de seguridad.md.
```

---

# 👤 Fase 5 — Módulo `models/player.py`

## Modelo del jugador

```
Crea la clase `Player` con los atributos:
- name: nombre del jugador
- hand: lista de cartas en mano
- score: puntuación acumulada
Incluye métodos para robar carta, descartar carta y mostrar la mano.
```

---

# 🖥️ Fase 6 — Módulo `ui/`

## Interfaz de terminal (`terminal.py`)

```
Crea un módulo `terminal.py` que gestione la entrada/salida del juego en consola.
Debe mostrar:
- El estado actual de la mano del jugador
- Las opciones disponibles en cada turno
- Mensajes de fin de ronda y puntuaciones
Usa caracteres especiales o colores ANSI para mejorar la legibilidad.
```

## Interfaz genérica (`interface.py`)

```
Define una clase base abstracta `GameInterface` con los métodos:
- show_hand(player)
- ask_action(options)
- show_message(message)
Implementa `TerminalInterface` que herede de ella para la versión de consola.
Esto permitirá añadir en el futuro interfaces gráficas u online.
```

---

# 🧪 Fase 7 — Tests con Pytest

## Generación de tests unitarios

```
Genera tests unitarios con pytest para cada uno de estos módulos:
- core/cards.py → test_cards.py
- core/engine.py → test_engine.py
- core/validator.py → test_validator.py
- models/player.py → test_player.py
- ui/terminal.py → test_terminal.py
- ui/interface.py → test_interface.py
- main.py → test_main.py
Cubre casos normales, casos límite y casos de error.
```

## Configuración de pytest

```
Crea un archivo pytest.ini con la configuración básica para el proyecto:
- directorio de tests
- marcadores personalizados si los hay
- cobertura mínima recomendada
También crea conftest.py con fixtures reutilizables (mazo, jugadores, engine de prueba).
```

---

# 🔒 Fase 8 — Seguridad

## Revisión de errores de seguridad

```
Analiza el proyecto completo en busca de posibles vulnerabilidades o errores de seguridad:
- Entradas de usuario no validadas
- Accesos a listas fuera de índice
- Estados inválidos del juego
Documenta los hallazgos en docs/Errores de seguridad.md con descripción, riesgo y solución propuesta.
```

---

# 🔧 Fase 9 — Punto de Entrada (`main.py`)

## Arranque del juego

```
Crea el archivo main.py como punto de entrada del juego.
Debe:
- Pedir el número de jugadores y sus nombres
- Inicializar el GameEngine con los jugadores y la interfaz de terminal
- Lanzar el bucle principal de la partida
- Mostrar el ganador al finalizar
```

---

# 📦 Dependencias (`requirements.txt`)

## Generación de dependencias

```
Genera el archivo requirements.txt para el proyecto Juego_Chincón en Python.
Incluye únicamente las dependencias necesarias: pytest y cualquier librería
de terminal o utilidad que se haya usado. Usa versiones estables actuales.
```

---

# 💡 Prompts de Refactorización y Mejora

```
Revisa el código de engine.py y refactoriza para mejorar la separación de responsabilidades.
El motor no debe conocer detalles de la UI; usa callbacks o un sistema de eventos simple.
```

```
Añade docstrings en formato Google/NumPy a todas las clases y métodos públicos del proyecto.
```

```
Optimiza el método de detección de combinaciones válidas en validator.py.
Actualmente tiene complejidad O(n!), busca una solución más eficiente.
```

---

*Documento generado como referencia del proceso de desarrollo asistido por IA del proyecto Juego_Chincón.*