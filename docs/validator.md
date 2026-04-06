# ✅ core/validator.py

Módulo de validación y cálculo de puntuaciones. Determina combinaciones válidas (escaleras y grupos) y calcula la puntuación óptima de una mano.

---

# Descripción

`Validador` es una clase de métodos de clase (sin instancia) que encapsula toda la lógica de evaluación de manos. Se encarga de reconocer combinaciones válidas del Chinchón y encontrar la distribución de cartas que minimiza los puntos de un jugador.

---

# `Validador`

## Constante de clase

```python
Validador.ORDEN = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 10:8, 11:9, 12:10}
```

Mapea los valores de carta a su posición ordinal en la baraja española, resolviendo el salto del 7 al 10.

---

# Métodos

## `es_escalera(cartas) → bool`
Determina si un conjunto de cartas forma una **escalera válida**.

Condiciones requeridas:
- Mínimo **3 cartas**.
- Todas del **mismo palo**.
- Valores **consecutivos** según `ORDEN`.
- **Sin comodines**.

```python
from core.cards import Carta

cartas = [Carta('Oros', 5), Carta('Oros', 6), Carta('Oros', 7)]
Validador.es_escalera(cartas)   # → True

cartas = [Carta('Oros', 5), Carta('Copas', 6), Carta('Oros', 7)]
Validador.es_escalera(cartas)   # → False (palos distintos)
```

---

## `es_grupo(cartas) → bool`
Determina si un conjunto de cartas forma un **grupo válido**.

Condiciones requeridas:
- Mínimo **3 cartas**.
- Todas con el **mismo valor**.
- **Sin comodines**.

```python
cartas = [Carta('Oros', 7), Carta('Copas', 7), Carta('Espadas', 7)]
Validador.es_grupo(cartas)   # → True

cartas = [Carta('Oros', 7), Carta('Copas', 7)]
Validador.es_grupo(cartas)   # → False (menos de 3 cartas)
```

---

## `calcular_puntos_optimos(mano) → tuple[int, bool]`
Calcula la **puntuación mínima posible** para una mano dada.

Retorna una tupla `(puntos, es_chinchon)`:

| Valor         | Descripción                                                   |
|---------------|---------------------------------------------------------------|
| `puntos`      | Suma de puntos de las cartas no incluidas en ningún combo     |
| `es_chinchon` | `True` si existe un combo que agrupa las 7 cartas (Chinchón) |

En caso de **Chinchón**, los puntos retornados son `-10` (bonificación especial).

```python
puntos, es_chinchon = Validador.calcular_puntos_optimos(jugador.mano)

if es_chinchon:
    print("¡Chinchón! -10 puntos")
else:
    print(f"Puntos de la mano: {puntos}")
```

> ⚠️ La implementación actual del algoritmo de búsqueda de subconjuntos óptimos está marcada como pendiente de desarrollo completo. Actualmente retorna la suma total de puntos sin restar combos intermedios.

---

## `_buscar_combos(mano) → List[tuple]` *(privado)*
Enumera todas las combinaciones válidas (grupos o escaleras) posibles dentro de una mano, de tamaño 3 a 7.

Usado internamente por `calcular_puntos_optimos()` para detectar el Chinchón.

```python
combos = Validador._buscar_combos(mano)
# Retorna lista de tuplas de Carta que forman grupos o escaleras válidas
```

---

# Ejemplo de uso completo

```python
from core.validator import Validador
from core.cards import Carta

mano = [
    Carta('Oros', 1), Carta('Oros', 2), Carta('Oros', 3),
    Carta('Copas', 7), Carta('Copas', 7), Carta('Espadas', 7),
    Carta('Bastos', 10)
]

puntos, chinchon = Validador.calcular_puntos_optimos(mano)
print(f"Puntos: {puntos}, Chinchón: {chinchon}")
```

---

# Dependencias

| Módulo      | Uso                                                  |
|-------------|------------------------------------------------------|
| `itertools` | Generación de combinaciones en `_buscar_combos()`    |