Para asegurar que la lógica de tu juego de Chinchón sea robusta, he preparado una guía de pruebas estructurada. Cubriremos desde la mecánica de los comodines hasta los escenarios límite del motor del juego.

# 1. Pruebas de Comodines (Wildcards)

El objetivo es verificar que el sistema reconozca el comodín en diferentes posiciones y ejecute correctamente la regla de   eliminación.

| Caso de Prueba | Descripción | Resultado Esperado |
| :--- | :--- | :--- |
| **Comodín en Tercia** | `[7♥, Joker, 7♣]` | El sistema debe validar la tercia correctamente asignando el valor 7 al Joker. |
| **Comodín en Escalera** | `[4♦, 5♦, Joker, 7♦]` | Debe completar la secuencia como un **6♦**. |
| **Comodín en Extremo** | `[Joker, 2♠, 3♠]` | Debe reconocerse como **1♠** o como el inicio válido de la secuencia. |
| **Comodín de Eliminación** | Jugador con Joker en mano al cerrar otro jugador. | El Joker debe sumar **25 puntos** (penalización) en lugar de 0 o su valor nominal. |
| **Múltiples Comodines** | `[5♣, Joker, Joker, 8♣]` | El sistema debe permitir dos comodines en una misma jugada (según reglas configuradas). |
| **Chinchón Completo** | Escalera de 7 cartas del mismo palo (sin comodín). | El jugador gana la partida automáticamente o resta **-50 puntos**. |
| **Mazo Vacío** | Agotar todas las cartas del mazo de robo. | El descarte debe barajarse automáticamente para regenerar el mazo de robo. |
| **Un solo jugador** | Iniciar partida sin oponentes o desconexión masiva. | El sistema debe manejar el estado de espera o finalizar la sesión sin errores de ejecución (null pointers). |

# 2. Escenarios de "Chinchón" Completo

El Chinchón ocurre cuando un jugador combina las 7 cartas (generalmente una escalera de 7 del mismo palo).

- Chinchón Limpio: 7 cartas consecutivas del mismo palo sin comodines.
    
    Resultado: El jugador gana la partida automáticamente o resta -25/-50 puntos.

- Chinchón con Comodín: 7 cartas combinadas usando un Joker.
    
    Resultado: Se resta el puntaje correspondiente, pero no suele terminar la partida de forma fulminante como el limpio.

- Cierre con 0 puntos: El jugador acomoda sus 7 cartas en dos grupos (ej. tercia y cuarta) 
pero no es una escalera única.         
    
    Resultado: Se restan 10 puntos (o regla estándar) pero no es "Chinchón".

# 3. Casos Edge (Casos Límite)

Estos casos suelen romper la lógica del flujo si no están bien controlados.

- A. Mazo Vacío (Pozo de Robo)
¿Qué pasa cuando se acaba el mazo de robo y nadie ha cerrado?

    - Acción: Agotar todas las cartas del mazo.
    
    - Comportamiento esperado: El mazo de descarte (basura) debe barajarse automáticamente (excepto la última carta tirada) para formar un nuevo mazo de robo.

- B. Un Solo Jugador
Aunque el Chinchón es multijugador, el sistema debe manejar este estado (común en modo práctica o errores de red).

    - Acción: Iniciar partida con 1 solo ID de usuario.
    
    - Comportamiento esperado: El sistema debe impedir el inicio o, en modo práctica, permitir el flujo de turnos sin colapsar al intentar "pasar el turno" al siguiente ID inexistente.
    
- C. Cartas en Mano al Cerrar

    - Cierre con Carta de Descarte: Probar cerrar cuando la carta que sobra es un Joker.
    - Puntos exactos: Verificar que si un jugador llega exactamente al límite de puntos (ej. 100), sea eliminado inmediatamente 
    
# 4. Matriz de Validación Técnica

Si estás automatizando estas pruebas, asegúrate de verificar estos estados en tu objeto GameState:

    1. can_close: Debe ser true solo si los puntos no combinados son $\le 5$.
    
    2. calculate_score: La función debe retornar 25 si detecta un Joker en la lista de cartas no combinadas del perdedor.
    
    3. deck_reset: Disparar un evento cuando deck.length === 0.