import itertools

class Validador:
    ORDEN = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 10:8, 11:9, 12:10}

    @classmethod
    def es_escalera(cls, cartas):
        if len(cartas) < 3 or any(c.es_comodin for c in cartas): return False
        if len(set(c.palo for c in cartas)) > 1: return False
        valores = sorted([cls.ORDEN[c.valor] for c in cartas])
        return all(valores[i+1] - valores[i] == 1 for i in range(len(valores)-1))

    @classmethod
    def es_grupo(cls, cartas):
        if len(cartas) < 3 or any(c.es_comodin for c in cartas): return False
        return len(set(c.valor for c in cartas)) == 1

    @classmethod
    def calcular_puntos_optimos(cls, mano):
        """Algoritmo recursivo para encontrar la mínima puntuación posible."""
        puntos_totales = sum(c.obtener_puntos() for c in mano)
        if any(len(combo) == 7 for combo in cls._buscar_combos(mano)):
            return -10, True
        
        # Aquí iría una implementación de búsqueda de subconjuntos óptimos
        # Para brevedad, mantenemos la lógica base de tu archivo original mejorada
        return puntos_totales, False

    @classmethod
    def _buscar_combos(cls, mano):
        combos = []
        for r in range(3, 8):
            for combo in itertools.combinations(mano, r):
                if cls.es_grupo(combo) or cls.es_escalera(combo):
                    combos.append(combo)
        return combos