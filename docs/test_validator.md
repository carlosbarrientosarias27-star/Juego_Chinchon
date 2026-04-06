# 🧪 tests/test_validator.py

Tests unitarios para `core/validator.py`. Verifica la detección de escaleras, grupos, cálculo de puntuación óptima y detección de Chinchón.

---

# Módulo bajo prueba
`core.validator` → `Validador`

---

# Helper

## `crear_carta(valor, palo, es_comodin=False) → MagicMock`
Función auxiliar que genera cartas mock con los atributos `valor`, `palo`, `es_comodin` y `obtener_puntos()` configurados. Valores ≤ 7 valen su valor nominal; valores > 7 valen `10`.

---

# Clase `TestValidador`

### Escaleras

## `test_es_escalera_valida`
Verifica que 3 cartas consecutivas del mismo palo (`1, 2, 3` de Oros) sean reconocidas como escalera válida.

## `test_es_escalera_distinto_palo`
Verifica que cartas de palos distintos **no** formen escalera, aunque los valores sean consecutivos.

## `test_es_escalera_salto_numerico`
Verifica que valores no consecutivos (`1, 2, 4`) **no** sean escalera válida.

## `test_es_escalera_con_comodin`
Verifica que una secuencia que contenga un comodín **no** sea reconocida como escalera (comportamiento actual del validador).

---

### Grupos

## `test_es_grupo_valido`
Verifica que 3 cartas del mismo valor en palos distintos (`5 de Oros/Copas/Bastos`) formen un grupo válido.

## `test_es_grupo_insuficiente`
Verifica que un par de cartas (2 cartas) **no** sea suficiente para formar un grupo válido.

---

### Puntuación y Chinchón

## `test_calcular_puntos_sin_combos`
Verifica que sin combinaciones válidas, `calcular_puntos_optimos()` sume todos los puntos de la mano (`1 + 10 = 11`) y retorne `chinchon = False`.

## `test_detectar_chinchon`
Verifica que una mano de 7 cartas que forman una escalera completa (`1–7` de Oros) sea detectada como Chinchón: retorna `(-10, True)`.

---

### Búsqueda de combinaciones

## `test_buscar_combos_existentes`
Verifica que `_buscar_combos()` identifique la escalera `1, 2, 3` de Bastos dentro de una mano mixta, y que todas las cartas del combo encontrado pertenezcan al palo `"Bastos"`.

---

# Ejecución

```bash
pytest tests/test_validator.py -v
```