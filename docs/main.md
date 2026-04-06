# 🚀 main.py

Punto de entrada de la aplicación. Inicializa la UI y arranca la partida de Chinchón.

---

# Descripción

`main.py` actúa como el punto de entrada del programa. Recoge los datos iniciales por consola (número de jugadores y sus nombres), instancia los componentes principales y lanza el bucle de juego.

---

# `iniciar_partida()`

Función principal que orquesta el arranque del juego:

1. Crea una instancia de `TerminalUI` y limpia la pantalla.
2. Solicita al usuario el número de jugadores (2–4) y sus nombres.
3. Instancia el motor `JuegoChinchon` con los nombres y la UI.
4. Llama a `juego.jugar()` para iniciar el bucle principal.

```python
iniciar_partida()
```

**Flujo de ejecución:**
```
Limpiar pantalla
↓
Pedir número de jugadores (2-4)
↓
Pedir nombre de cada jugador
↓
Crear JuegoChinchon(nombres, ui)
↓
juego.jugar()  →  bucle principal en core/engine.py
```

---

# Ejecución

```bash
python main.py
```

Salida esperada al iniciar:

```
--- CHINCHÓN PROFESIONAL ---
Número de jugadores (2-4): 3
Nombre J1: Ana
Nombre J2: Luis
Nombre J3: María
```

---

# Dependencias

| Módulo           | Uso                              |
|------------------|----------------------------------|
| `core.engine`    | Motor principal `JuegoChinchon`  |
| `ui.terminal`    | Interfaz de consola `TerminalUI` |