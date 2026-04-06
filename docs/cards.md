# 🃏 core/cards.py

Módulo de estructuras de datos para la baraja española con soporte para comodines.

---

# Descripción

Implementa las piezas fundamentales del juego: una carta inmutable (`Carta`) y una baraja completa con gestión automática del mazo y pila de descartes (`Baraja`). Contiene **40 cartas** de baraja española más **4 comodines** (44 en total).

---

# `Carta` — dataclass inmutable

```python
@dataclass(frozen=True)
class Carta:
    palo: Optional[str] = None
    valor: Optional[int] = None
    es_comodin: bool = False
    id_comodin: Optional[int] = None
```

`frozen=True` garantiza que las cartas no puedan modificarse tras su creación, haciéndolas seguras para usar como claves de diccionario o elementos de conjuntos.

| Campo        | Tipo            | Descripción                                     |
|--------------|-----------------|-------------------------------------------------|
| `palo`       | `Optional[str]` | `'Oros'`, `'Copas'`, `'Espadas'` o `'Bastos'`  |
| `valor`      | `Optional[int]` | Valor numérico: 1–7, 10–12 (sin 8 ni 9)        |
| `es_comodin` | `bool`          | `True` si la carta es un comodín               |
| `id_comodin` | `Optional[int]` | Identificador único del comodín (1–4)          |

### Métodos

## `obtener_puntos() → int`
Devuelve el valor en puntos de la carta. Los comodines siempre retornan `0`.

```python
Carta('Oros', 7).obtener_puntos()                      # → 7
Carta(es_comodin=True, id_comodin=1).obtener_puntos()  # → 0
```

---

# `Baraja`

Gestiona el ciclo de vida completo del mazo: inicialización, reinicio entre rondas, robo y reabastecimiento automático desde los descartes.

### Constantes

```python
Baraja.PALOS   = ['Oros', 'Copas', 'Espadas', 'Bastos']
Baraja.VALORES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
```

> ⚠️ La baraja española no incluye los valores 8 ni 9.

### Atributos de instancia

| Atributo    | Tipo          | Descripción                        |
|-------------|---------------|------------------------------------|
| `cartas`    | `List[Carta]` | Mazo disponible para robar         |
| `descartes` | `List[Carta]` | Pila de cartas descartadas         |

### Métodos

## `reiniciar()`
Prepara la baraja para una **nueva ronda**, limpiando completamente la pila de descartes y regenerando las 44 cartas (40 normales + 4 comodines) mezcladas aleatoriamente.

Debe llamarse al inicio de cada ronda antes de repartir.

```python
baraja = Baraja()
# ... transcurre una ronda ...
baraja.reiniciar()  # Lista para la siguiente ronda
```

## `robar() → Optional[Carta]`
Extrae y retorna la carta superior del mazo.

- Si el mazo está vacío, **rebaraja automáticamente** los descartes (reservando la última carta descartada en la pila).
- Retorna `None` si no hay cartas disponibles en ningún lado.

```python
baraja = Baraja()
carta = baraja.robar()       # Carta aleatoria
baraja.descartes.append(carta)
```

## `_reabastecer_mazo()` *(privado)*
Mueve los descartes al mazo y los baraja, conservando siempre la última carta descartada visible. Llamado internamente por `robar()`.

---

# Ejemplo de uso

```python
from core.cards import Baraja

baraja = Baraja()

# Robar y descartar
carta = baraja.robar()
print(f"{carta.palo} {carta.valor}")  # ej: "Espadas 3"
print(carta.obtener_puntos())         # ej: 3
baraja.descartes.append(carta)

# Robar del descarte
tope = baraja.descartes.pop()

# Preparar nueva ronda
baraja.reiniciar()
```

---

# Dependencias

| Módulo        | Uso                       |
|---------------|---------------------------|
| `random`      | Barajar el mazo           |
| `dataclasses` | Definición de `Carta`     |
| `typing`      | Anotaciones de tipo       |