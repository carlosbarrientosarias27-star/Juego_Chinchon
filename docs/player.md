# 👤 models/player.py

Modelo de datos que representa a un participante en la partida de Chinchón.

---

# Descripción

`Jugador` es un dataclass que mantiene todo el estado de un jugador durante la partida: su mano de cartas, puntuación acumulada, estado de eliminación y registro de comodines de cerveza ya consumidos.

---

# `Jugador` — dataclass

```python
@dataclass
class Jugador:
    nombre: str
    puntos: int = 0
    eliminado: bool = False
    mano: List[Carta] = field(default_factory=list)
    uso_comodin: Dict[int, bool] = field(default_factory=lambda: {...})
```

## Atributos de instancia

| Atributo      | Tipo              | Descripción                                          |
|---------------|-------------------|------------------------------------------------------|
| `nombre`      | `str`             | Nombre del jugador                                   |
| `puntos`      | `int`             | Puntuación acumulada (empieza en 0)                  |
| `eliminado`   | `bool`            | `True` si el jugador ha sido eliminado de la partida |
| `mano`        | `List[Carta]`     | Cartas actuales en mano                              |
| `uso_comodin` | `Dict[int, bool]` | Registro de comodines de cerveza consumidos          |

## Estado inicial de `uso_comodin`

| ID | Nombre          | Valor inicial |
|----|-----------------|---------------|
| 1  | Estrella Galicia | `False`       |
| 2  | Alhambra Verde  | `False`        |
| 3  | 1906            | `False`        |
| 4  | SIN CERVEZA     | `False`        |

---

### Métodos

## `añadir_a_mano(carta: Carta) → None`
Agrega una carta al final de la mano del jugador.

```python
jugador.añadir_a_mano(carta_robada)
```

---

## `extraer_de_mano(indice: int) → Carta`
Elimina y retorna la carta en la posición indicada.

- Lanza `IndexError` si el índice está fuera de rango.

```python
carta_descartada = jugador.extraer_de_mano(2)
```

---

## `tiene_comodin_usado(id_comodin: int) → bool`
Verifica si el jugador ya ha activado el efecto de un comodín específico.

```python
if not jugador.tiene_comodin_usado(1):
    # Aplicar efecto de Estrella Galicia
```

---

## `marcar_comodin_usado(id_comodin: int) → None`
Registra un comodín como ya procesado. No tiene efecto si el ID no existe.

```python
jugador.marcar_comodin_usado(1)
```

---

# Propiedades

## `cantidad_cartas → int`
Retorna el número de cartas que el jugador tiene actualmente en mano.

```python
print(jugador.cantidad_cartas)  # ej: 7
```

---

# Representación en cadena

`__str__` retorna un resumen legible del estado del jugador:

```python
str(jugador)
# → "Jugador: Ana | Estado: 15 pts | Cartas: 7"
# → "Jugador: Luis | Estado: ELIMINADO | Cartas: 0"
```

---

# Ejemplo de uso

```python
from models.player import Jugador
from core.cards import Baraja

baraja = Baraja()
jugador = Jugador("Ana")

# Repartir 7 cartas
for _ in range(7):
    jugador.añadir_a_mano(baraja.robar())

print(jugador.cantidad_cartas)   # → 7

# Descartar la primera carta
descarte = jugador.extraer_de_mano(0)

# Verificar comodín
if not jugador.tiene_comodin_usado(3):
    jugador.marcar_comodin_usado(3)

print(jugador)
# → "Jugador: Ana | Estado: 0 pts | Cartas: 6"
```

---

# Dependencias

| Módulo        | Uso                                    |
|---------------|----------------------------------------|
| `dataclasses` | Definición del dataclass y `field()`   |
| `typing`      | Anotaciones `List` y `Dict`            |
| `core.cards`  | Tipo `Carta` para la mano del jugador  |